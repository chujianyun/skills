#!/usr/bin/env python3
"""Capture the Chinese Dify Cloud navigation into a fresh Baize staging directory.

Python 3.10+, standard library only. This writes staging files, never a live Skill.
A resume uses cached responses from this staging; use a new directory for updates.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = 'https://docs.dify.ai'
ROOT_INDEX = BASE + '/_llms/zh/cloud.txt'
LINK = re.compile(r'^- \[(.*?)\]\((https://docs\.dify\.ai/[^)]+)\)(?::\s*(.*))?$')
IMAGE = re.compile(r'!\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)')
MDLINK = re.compile(r'(?<!!)\[([^\]\n]*)\]\(([^\s)]+)(?:\s+"[^"]*")?\)')
HTMLSRC = re.compile(r'\b(?:src|poster)=["\']([^"\']+)["\']')
PREFIX = re.compile(r'\A> ## Documentation Index\n> Fetch[^\n]*\n> Use[^\n]*\n\n')
ALLOWED_ASSETS = {'assets-docs.dify.ai', 'docs.dify.ai', 'mintcdn.com', 'cdn.mintlify.com', 'mintlify.s3.us-west-1.amazonaws.com', 'raw.githubusercontent.com', 'i.ibb.co', 'help-static-aliyun-doc.aliyuncs.com'}


def safe_name(text: str) -> str:
    text = re.sub(r'[\x00-\x1f/\\:*?"<>|]', ' ', html.unescape(text))
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip(' .') or '概述'


def canonical(url: str) -> str:
    u = urllib.parse.urlsplit(url)
    path = u.path.rstrip('/')
    path = re.sub(r'\.(?:md|mdx|html)$', '', path)
    return urllib.parse.urlunsplit((u.scheme, u.netloc, path, '', ''))


def inline_parts(text: str):
    last = 0
    for match in re.finditer(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)', text, re.S):
        if match.start() > last:
            yield False, text[last:match.start()]
        yield True, match[0]
        last = match.end()
    if last < len(text):
        yield False, text[last:]


def prose_parts(text: str):
    """Yield code/prose segments, retaining nested quoted Markdown fences verbatim."""
    chunk = []
    fence_char, fence_len = '', 0
    in_code = False
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(?:>\s*)*(`{3,}|~{3,})(.*)$', line)
        if marker and not in_code:
            if chunk:
                yield from inline_parts(''.join(chunk))
                chunk = []
            in_code = True
            fence_char, fence_len = marker[1][0], len(marker[1])
            chunk.append(line)
        elif marker and in_code and marker[1][0] == fence_char and len(marker[1]) >= fence_len and not marker[2].strip():
            chunk.append(line)
            yield True, ''.join(chunk)
            chunk, in_code = [], False
        else:
            chunk.append(line)
    if chunk:
        if in_code:
            yield True, ''.join(chunk)
        else:
            yield from inline_parts(''.join(chunk))


def asset_url(base: str, target: str) -> str:
    url = urllib.parse.urljoin(base, html.unescape(target).replace('\\&', '&'))
    parts = urllib.parse.urlsplit(url)
    if parts.netloc == 'mintcdn.com' and '/images/' in parts.path:
        # Use the public upstream source file, without temporary CDN signatures.
        path = 'images/' + parts.path.split('/images/', 1)[1]
        return 'https://raw.githubusercontent.com/langgenius/dify-docs/main/' + path
    return url


class Capture:
    def __init__(self, staging: Path, workers: int):
        self.staging, self.workers = staging, workers
        self.cache = staging / '_capture-cache'
        self.cache.mkdir(parents=True, exist_ok=True)
        self.pages: dict[str, dict] = {}
        self.indexes: dict[str, str] = {}

    def get(self, url: str) -> bytes:
        cache = self.cache / hashlib.sha256(url.encode()).hexdigest()
        if cache.is_file():
            return cache.read_bytes()
        # Initial attempt plus at most two retries. Authorization/rate errors stop.
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'DifyWikiOfflineCapture/1.0'})
                with urllib.request.urlopen(req, timeout=45) as response:
                    data = response.read()
                if not data:
                    raise ValueError('Empty response: ' + url)
                tmp = cache.with_suffix('.tmp')
                tmp.write_bytes(data)
                tmp.replace(cache)
                return data
            except urllib.error.HTTPError as exc:
                if exc.code in {401, 403, 429} or attempt == 2:
                    raise
            except (OSError, ValueError):
                if attempt == 2:
                    raise
            time.sleep(attempt + 1)
        raise RuntimeError(url)

    def map_index(self, url: str, prefix: tuple[str, ...] = ()) -> None:
        if url in self.indexes:
            return
        text = self.get(url).decode('utf-8')
        self.indexes[url] = text
        headings: dict[int, str] = {}
        for line in text.splitlines():
            heading = re.match(r'^(#{2,})\s+(.*)', line)
            if heading:
                depth, label = len(heading[1]), heading[2].strip()
                headings = {k: v for k, v in headings.items() if k < depth}
                if label:
                    headings[depth] = safe_name(label)
                continue
            match = LINK.match(line)
            if not match:
                continue
            title, link, summary = match.groups()
            if '/_llms/' in link:
                if not link.startswith(BASE + '/_llms/zh/cloud/'):
                    raise ValueError('Unexpected index scope: ' + link)
                # Subindexes are independent documents; their H2 repeats this root.
                child_prefix = ('开发者资源',) if '/api.txt' in link else ()
                self.map_index(link, child_prefix)
                continue
            if not link.endswith('.md'):
                continue
            groups = prefix + tuple(v for k, v in sorted(headings.items()) if v != 'Cloud')
            if not groups or groups[0] not in {'使用', '学习', '开发者资源'}:
                raise ValueError('Unexpected navigation branch: ' + repr(groups))
            url_key = canonical(link)
            local = '/'.join((*groups, safe_name(title) + '.md'))
            if url_key in self.pages:
                continue
            self.pages[url_key] = {
                'title': title, 'source_url': url_key,
                'source_path': urllib.parse.urlsplit(url_key).path,
                'local_path': local, 'summary': summary or '',
                'keywords': list(dict.fromkeys((*groups, urllib.parse.urlsplit(url_key).path.rsplit('/', 1)[-1]))),
                '_markdown_url': link,
            }
        paths = [p['local_path'] for p in self.pages.values()]
        if len(paths) != len(set(paths)):
            duplicates = {p for p in paths if paths.count(p) > 1}
            raise ValueError('Navigation title collision: ' + repr(duplicates))

    def map_navigation(self) -> None:
        config_url = 'https://raw.githubusercontent.com/langgenius/dify-docs/main/docs.json'
        config = json.loads(self.get(config_url))
        language = next(x for x in config['navigation']['languages'] if x['language'] == 'zh')
        product = next(x for x in language['products'] if x['product'] == 'Cloud')
        direct, operations = {}, set()
        def walk(node, groups=()):
            if isinstance(node, str):
                if node.startswith('zh/'):
                    direct.setdefault(BASE + '/' + node, groups)
                elif re.match(r'^(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD) /', node):
                    operations.add(node)
            elif isinstance(node, list):
                for child in node:
                    walk(child, groups)
            elif isinstance(node, dict):
                label = next((node[k] for k in ('tab', 'item', 'group') if node.get(k)), None)
                nested = groups + (safe_name(label),) if label and label.strip() else groups
                if node.get('root'):
                    walk(node['root'], nested)
                for key in ('pages', 'groups', 'menu'):
                    walk(node.get(key, []), nested)
        walk(product['tabs'])
        # The llms index can omit a navigable homepage. Merge it, rather than assuming an alias.
        self.navigation_only = set(direct) - set(self.pages)
        for url, groups in direct.items():
            if url in self.pages:
                continue
            body = self.get(url + '.md').decode('utf-8')
            title = re.search(r'^#\s+(.+)', body, re.M)
            if not title:
                raise ValueError('Navigation-only page has no title: ' + url)
            self.pages[url] = {'title': title[1], 'source_url': url,
                'source_path': urllib.parse.urlsplit(url).path,
                'local_path': '/'.join((*groups, safe_name(title[1]) + '.md')),
                'summary': '官方导航中的补充入口', 'keywords': list(groups), '_markdown_url': url + '.md'}
        generated = set(self.pages) - set(direct)
        if len(generated) != len(operations):
            raise ValueError(f'Navigation/index mismatch: {len(generated)} generated pages vs {len(operations)} operations')
        spec = json.loads(self.get(BASE + '/zh/api-reference/openapi_service.json'))
        for operation in operations:
            method, path = operation.split(' ', 1)
            if method.lower() not in spec['paths'].get(path, {}):
                raise ValueError('Navigation operation absent from schema: ' + operation)
        paths = [page['local_path'] for page in self.pages.values()]
        if len(paths) != len(set(paths)):
            raise ValueError('Navigation-only page creates a title collision')
        self.navigation_report = {'config_url': config_url, 'direct_pages': len(direct),
                                  'generated_api_operations': len(operations), 'merged_pages': len(self.pages)}
        self.expected_operations = operations

    def capture(self) -> None:
        if (self.staging / 'inventory.json').exists():
            raise ValueError('Completed staging already exists; use a fresh directory for a new snapshot')
        self.map_index(ROOT_INDEX)
        self.map_navigation()
        print(f'Discovered {len(self.pages)} pages across {len(self.indexes)} indexes', flush=True)
        (self.staging / 'navigation-discovered.json').write_text(json.dumps({
            'source_root': BASE + '/zh/cloud', 'indexes': list(self.indexes),
            'pages': [{k: v for k, v in page.items() if not k.startswith('_')}
                      for page in self.pages.values()]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # Cross-check the independently published sitemap; llms indexes define scope.
        sitemap = self.get(BASE + '/sitemap.xml')
        locations = {canonical(e.text or '') for e in ET.fromstring(sitemap).iter() if e.tag.endswith('}loc')}
        absent = set(self.pages) - locations
        unexpected_absent = absent - self.navigation_only
        if unexpected_absent:
            raise ValueError(f'Index pages absent from sitemap: {sorted(unexpected_absent)}')
        raw, failed = {}, []
        def fetch_page(item):
            key, page = item
            body = self.get(page['_markdown_url']).decode('utf-8')
            if '<!doctype html' in body[:1000].lower() or not re.search(r'^#\s+\S', body, re.M):
                raise ValueError('Not a documentation body: ' + key)
            return key, PREFIX.sub('', body).replace('\n\nThis documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.', '')
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = {pool.submit(fetch_page, item): item[0] for item in self.pages.items()}
            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                try:
                    key, text = future.result()
                    raw[key] = text
                except Exception as exc:
                    failed.append({'url': futures[future], 'error': str(exc)})
                    print(f'Failed: {futures[future]}: {exc}', file=sys.stderr, flush=True)
                    if isinstance(exc, urllib.error.HTTPError) and exc.code in {401, 403, 429}:
                        blocked = sum(any(f'HTTP Error {code}' in e['error'] for code in (401, 403, 429)) for e in failed)
                        if blocked >= 3:
                            for pending in futures:
                                pending.cancel()
                            (self.staging/'capture-failures.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2))
                            raise ValueError('Repeated authorization/rate failures; remaining requests cancelled')
                if i % 25 == 0 or i == len(futures):
                    print(f'Pages {i}/{len(futures)}, failures {len(failed)}', flush=True)
        if failed:
            (self.staging/'capture-failures.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2))
            raise ValueError('Page capture failed; no inventory published. Resume after fixing the failure.')
        captured_operations = set()
        for text in raw.values():
            for method, path in re.findall(r'^`{3,}yaml\s+\S+\s+(get|post|put|patch|delete|options|head)\s+(/\S*)\s*$', text, re.M):
                captured_operations.add(method.upper() + ' ' + path)
        if captured_operations != self.expected_operations:
            raise ValueError('Rendered API operation coverage differs from source navigation')
        # Rewrite internal documentation links using complete canonical mapping.
        asset_urls = set()
        for key, text in raw.items():
            prose = ''.join(part for is_code, part in prose_parts(text) if not is_code)
            for match in list(IMAGE.finditer(prose)) + list(HTMLSRC.finditer(prose)):
                url = asset_url(key, match[1])
                parts = urllib.parse.urlsplit(url)
                if parts.scheme in {'http', 'https'} and parts.netloc not in ALLOWED_ASSETS:
                    if match.re is IMAGE:
                        raise ValueError('Review new embedded image host: ' + parts.netloc)
                    continue  # External interactive embeds stay online.
                if parts.scheme in {'http', 'https'} and parts.netloc in ALLOWED_ASSETS:
                    if parts.query:
                        raise ValueError('Review query-bearing asset URL before persisting: ' + parts.netloc)
                    asset_urls.add(url)
        asset_map = {}
        for url in sorted(asset_urls):
            suffix = Path(urllib.parse.unquote(urllib.parse.urlsplit(url).path)).suffix.lower()
            if not re.fullmatch(r'\.[a-z0-9]{1,8}', suffix):
                suffix = '.bin'
            asset_map[url] = 'images/' + hashlib.sha256(url.encode()).hexdigest()[:24] + suffix
        print(f'Downloading {len(asset_map)} embedded assets', flush=True)
        def fetch_asset(item):
            url, relative = item
            data = self.get(url)
            if data[:100].lstrip().lower().startswith(b'<!doctype html'):
                raise ValueError('Asset returned HTML: ' + url)
            dest = self.staging / 'assets' / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return len(data)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = {pool.submit(fetch_asset, item): item[0] for item in asset_map.items()}
            size = 0
            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                try:
                    size += future.result()
                except Exception as exc:
                    failed.append({'url': futures[future], 'error': str(exc)})
                    print(f'Failed: {futures[future]}: {exc}', file=sys.stderr, flush=True)
                    if isinstance(exc, urllib.error.HTTPError) and exc.code in {401, 403, 429}:
                        blocked = sum(any(f'HTTP Error {code}' in e['error'] for code in (401, 403, 429)) for e in failed)
                        if blocked >= 3:
                            for pending in futures:
                                pending.cancel()
                            (self.staging/'capture-failures.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2))
                            raise ValueError('Repeated authorization/rate failures; remaining requests cancelled')
                if i % 40 == 0 or i == len(futures):
                    print(f'Assets {i}/{len(futures)}, {size/1024/1024:.1f} MiB, failures {len(failed)}', flush=True)
        if failed:
            (self.staging/'capture-failures.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2))
            raise ValueError('Asset capture failed; no inventory published.')
        for key, page in self.pages.items():
            current = Path(page['local_path'])
            def rel_doc(match):
                label, target = match.groups()
                absolute = urllib.parse.urljoin(key, html.unescape(target))
                norm = canonical(absolute)
                if norm in self.pages:
                    rel = os.path.relpath(self.pages[norm]['local_path'], current.parent).replace(os.sep, '/')
                    frag = urllib.parse.urlsplit(absolute).fragment
                    return '[' + label + '](' + urllib.parse.quote(rel, safe='/') + ('#' + frag if frag else '') + ')'
                # Preserve non-scope links as absolute URLs; don't leave broken root-relative paths.
                if target.startswith('/'):
                    return '[' + label + '](' + absolute + ')'
                return match[0]
            parts = list(prose_parts(raw[key]))
            def rel_asset(match):
                target = match[1]
                url = asset_url(key, target)
                if url not in asset_map:
                    return match[0]
                relative = os.path.relpath(Path('../assets') / asset_map[url], current.parent).replace(os.sep, '/')
                start = match.start(1) - match.start()
                end = match.end(1) - match.start()
                return match[0][:start] + urllib.parse.quote(relative, safe='/') + match[0][end:]
            body = ''.join(part if is_code else HTMLSRC.sub(rel_asset, IMAGE.sub(rel_asset, MDLINK.sub(rel_doc, part)))
                           for is_code, part in parts)
            body = unicodedata.normalize('NFC', '\n'.join(l.rstrip() for l in body.splitlines())).rstrip() + '\n'
            dest = self.staging / 'docs' / page['local_path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body, encoding='utf-8')
        assets = [{'source_url': u, 'local_path': p} for u, p in asset_map.items()]
        # Preserve raw API schemas in addition to per-operation rendered reference pages.
        spec_url = BASE + '/zh/api-reference/openapi_service.json'
        spec = self.get(spec_url)
        json.loads(spec)
        spec_dest = self.staging / 'assets' / 'openapi_service.json'
        spec_dest.write_bytes(spec)
        assets.append({'source_url': spec_url, 'local_path': 'openapi_service.json'})
        # Keep upstream license verbatim; all copied pages remain CC BY 4.0.
        license_url = 'https://raw.githubusercontent.com/langgenius/dify-docs/main/LICENSE'
        license_data = self.get(license_url)
        if b'Attribution 4.0 International' not in license_data:
            raise ValueError('Review changed upstream license before publication')
        (self.staging/'assets'/'UPSTREAM-LICENSE.txt').write_bytes(license_data)
        assets.append({'source_url': license_url, 'local_path': 'UPSTREAM-LICENSE.txt'})
        inventory = {'schema_version': 1, 'source_root': BASE + '/zh/cloud',
                     'coverage': {'discovered': len(self.pages), 'captured': len(self.pages), 'failed': [],
                                  'excluded': [{'url': BASE + '/zh/product', 'reason': 'Separate self-host product/deployment navigation; outside selected Cloud tabs'},
                                               {'url': BASE + '/en', 'reason': 'Different language'},
                                               {'url': BASE + '/ja', 'reason': 'Different language'}]},
                     'pages': [{k: v for k, v in p.items() if not k.startswith('_')} for p in self.pages.values()],
                     'assets': assets}
        (self.staging/'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        report = {'indexes': list(self.indexes), 'sitemap_crosscheck': len(self.pages) - len(absent), 'navigation_only_pages': sorted(self.navigation_only), 'pages': len(self.pages),
                  'assets': len(assets), 'embedded_asset_bytes': size, 'navigation_crosscheck': self.navigation_report,
                  'branches': {b: sum(p['local_path'].startswith(b + '/') for p in self.pages.values()) for b in ['使用', '学习', '开发者资源']}}
        (self.staging/'capture-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir', required=True, type=Path)
    parser.add_argument('--workers', type=int, default=5, choices=range(1, 9))
    args = parser.parse_args()
    try:
        Capture(args.staging_dir.resolve(), args.workers).capture()
    except Exception as exc:
        print(f'Capture stopped: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Capture the Chinese Palantir Ontology navigation and official Markdown.

Uses only Python's standard library. Produces a Baize staging directory; does
not install, publish, or modify an existing skill. Cached responses permit a
bounded retry without changing the discovered scope.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time
import unicodedata
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ORIGIN = 'https://www.palantir.com'
ROOT = ORIGIN + '/docs/zh/foundry/ontology/overview/'
NEXT_DATA = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
FENCES = re.compile(r'(^```[^\n]*\n.*?^```[^\n]*$|^~~~[^\n]*\n.*?^~~~[^\n]*$)', re.M | re.S)
LINK = re.compile(r'(!?\[(?:\\.|[^\]\\])*\]\()(<[^>]+>|[^\s)]+)([^\n)]*\))')
ATTR = re.compile(r'((?:src|poster|href)=["\'])([^"\']+)(["\'])')
REF = re.compile(r'(^[ \t]*\[[^\]\n]+\]:[ \t]*)(\S+)', re.M)


class RenderedImages(HTMLParser):
    """Resolve locale-specific media using the rendered page, not URL guesses."""
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            source = dict(attrs).get('src', '')
            path = unquote(urlsplit(source).path)
            if path.startswith('/docs/resources/'):
                self.paths.add(path)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def fetch(url, target, retries=2):
    if target.is_file() and target.stat().st_size:
        return target.read_bytes()
    for attempt in range(retries + 1):
        try:
            request = Request(url, headers={'User-Agent': 'PalantirOntologyOfflineWiki/1.0', 'Accept': '*/*'})
            with urlopen(request, timeout=45) as response:
                if response.status != 200:
                    raise ValueError(f'HTTP {response.status}')
                data = response.read()
            if not data:
                raise ValueError('empty response')
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + '.part')
            temporary.write_bytes(data)
            temporary.replace(target)
            return data
        except Exception:
            if attempt == retries:
                raise
            time.sleep(attempt + 1)


def props_from_html(data):
    match = NEXT_DATA.search(data.decode('utf-8'))
    if not match:
        raise ValueError('missing official __NEXT_DATA__')
    return json.loads(match.group(1))['props']['pageProps']


def safe(value):
    value = unicodedata.normalize('NFC', value)
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', value).strip(' .') or 'untitled'


def navigation(items, parents=()):
    header = None
    for item in items:
        kind = item['type']
        if kind == 'header':
            header = item['text']
            continue
        above = parents + ((header,) if header else ())
        if kind == 'pageLink':
            yield {'title': item['link']['text'], 'source_path': '/docs' + item['link']['url'], 'groups': list(above)}
        elif kind not in ('section', 'pageGroup'):
            raise ValueError(f'unknown navigation type: {kind}')
        for key in ('items', 'pages'):
            if key in item:
                yield from navigation(item[key], above + (item.get('title') or item.get('text') or item['id'],))


def page_key(path):
    path = unquote(urlsplit(path).path)
    return re.sub(r'^/docs/(?:zh/)?', '/docs/', path).rstrip('/')


def asset_key(raw, context):
    raw = unquote(urlsplit(html.unescape(raw)).path)
    # Source Markdown retains the author's repository-relative media paths.
    match = re.search(r'(?:^|/)([\w-]+)-docs/(.+?)/media/(.+)$', raw)
    if match:
        return '/docs/resources/' + match[1] + '/' + match[2] + '/' + match[3]
    if raw.startswith('/docs/resources/'):
        return raw
    if raw.startswith('/resources/'):
        return '/docs' + raw
    match = re.match(r'(?:\./)?media/(.+)$', raw)
    if match:
        return '/docs/resources/foundry/' + context + '/' + match[1]
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--allow-missing-assets', action='store_true',
                        help='Only after the user explicitly accepts an incomplete media snapshot')
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be between 1 and 8')
    stage = args.staging_dir.expanduser().resolve()
    stage.mkdir(parents=True, exist_ok=True)
    cache = stage / 'capture-cache'
    overview = fetch(ROOT, cache / 'overview.html')
    initial = props_from_html(overview)
    pages = list(navigation(initial['sidebarNavProps']['items']))
    urls, paths = set(), set()
    for page in pages:
        page['source_url'] = ORIGIN + page['source_path']
        local = PurePosixPath(*(safe(x) for x in page['groups']), safe(page['title']) + '.md')
        if str(local).casefold() in paths:
            local = local.with_stem(local.stem + '-' + PurePosixPath(page['source_path']).name)
        if page['source_url'] in urls or str(local).casefold() in paths:
            raise ValueError('duplicate navigation URL or local path')
        urls.add(page['source_url']); paths.add(str(local).casefold())
        page['local_path'] = str(local)
    write_json(stage / 'navigation.json', pages)
    sitemap = fetch(ORIGIN + '/docs/sitemap.xml', cache / 'sitemap.xml')
    sitemap_paths = {urlsplit(x.text).path.rstrip('/') for x in ET.fromstring(sitemap).findall('{*}url/{*}loc')}
    absent = [p['source_url'] for p in pages if p['source_path'].rstrip('/') not in sitemap_paths]
    if absent:
        raise ValueError(f'navigation pages missing from sitemap: {absent}')
    print(f'MAP: {len(pages)} unique navigation pages; all present in official sitemap', flush=True)
    documents = {}
    failed = []

    def capture_page(page):
        key = hashlib.sha256(page['source_url'].encode()).hexdigest()
        data = fetch(page['source_url'], cache / 'pages' / (key + '.html'))
        props = props_from_html(data)
        rendered = RenderedImages()
        rendered.feed(data.decode('utf-8'))
        props['_rendered_media_paths'] = sorted(rendered.paths)
        markdown = props.get('markdown', '')
        if len(markdown.strip()) < 80:
            raise ValueError('empty or unexpectedly short Markdown')
        # Some upstream pages supply the title separately from their Markdown.
        if not re.search(r'^# ', markdown, re.M):
            props['markdown'] = '# ' + page['title'] + '\n\n' + markdown
        if props.get('categoryId') != 'ontology':
            raise ValueError(f'unexpected category: {props.get("categoryId")}')
        return page, props

    with futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(capture_page, page): page for page in pages}
        for n, job in enumerate(futures.as_completed(jobs), 1):
            page = jobs[job]
            try:
                _, props = job.result()
                documents[page['source_url']] = props
            except Exception as error:
                failed.append({'url': page['source_url'], 'error': f'{type(error).__name__}: {error}'})
            if n % 25 == 0 or n == len(pages):
                print(f'CAPTURE: {n}/{len(pages)}; failures={len(failed)}', flush=True)
    if failed:
        write_json(stage / 'capture-failures.json', failed)
        raise ValueError(f'{len(failed)} pages failed; no complete inventory generated')

    assets = {}
    asset_aliases = {}
    for props in documents.values():
        media_paths = set(props.get('docAssetMetadata', {}))
        rendered_paths = set(props['_rendered_media_paths'])
        media_paths.update(rendered_paths)
        for n, part in enumerate(FENCES.split(props['markdown'])):
            if n % 2:
                continue
            raw_targets = [match[2] for match in LINK.finditer(part)]
            raw_targets += [match[2] for match in ATTR.finditer(part)]
            raw_targets += [match[2] for match in REF.finditer(part)]
            for raw in raw_targets:
                parsed = urlsplit(html.unescape(raw.strip('<>')))
                if parsed.netloc and parsed.netloc not in ('www.palantir.com', 'palantir.com'):
                    continue
                key = asset_key(raw.strip('<>'), props['context'])
                if key:
                    localized = key.replace('/docs/resources/', '/docs/resources/zh/', 1)
                    if key not in media_paths and localized in rendered_paths:
                        asset_aliases[key] = localized
                        key = localized
                    media_paths.add(key)
        for path in media_paths:
            if not path.startswith('/docs/resources/'):
                raise ValueError(f'unknown asset path: {path}')
            local = unquote(path[len('/docs/resources/'):])
            if '..' in PurePosixPath(local).parts or PurePosixPath(local).is_absolute():
                raise ValueError('unsafe asset path')
            assets[path] = {'source_url': ORIGIN + quote(path, safe='/'), 'local_path': local}
    write_json(stage / 'asset-map.json', assets)
    print(f'ASSETS: {len(assets)} distinct official media resources', flush=True)

    def capture_asset(item):
        path, asset = item
        target = stage / 'assets' / asset['local_path']
        known_missing = cache / 'invalid-assets' / (hashlib.sha256(path.encode()).hexdigest() + '.html')
        # The same staging directory represents one capture. Reuse its bounded
        # failed attempts; a later refresh must start in a new staging directory.
        if known_missing.is_file() and not target.is_file():
            raise ValueError(f'official asset URL returned HTML instead of an image: {path}')
        for attempt in range(3):
            try:
                data = fetch(asset['source_url'], target, retries=0)
                if data.lstrip().startswith((b'<!DOCTYPE html', b'<html')):
                    invalid = cache / 'invalid-assets' / (hashlib.sha256(path.encode()).hexdigest() + '.html')
                    invalid.parent.mkdir(parents=True, exist_ok=True)
                    target.replace(invalid)
                    raise ValueError(f'official asset URL returned HTML instead of an image: {path}')
                return len(data)
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)

    asset_bytes = 0
    missing_assets = {}
    with futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(capture_asset, item): item for item in sorted(assets.items())}
        for n, job in enumerate(futures.as_completed(jobs), 1):
            try:
                asset_bytes += job.result()
            except Exception as error:
                key, asset = jobs[job]
                record = {'url': asset['source_url'], 'error': f'{type(error).__name__}: {error}'}
                failed.append(record)
                missing_assets[key] = record
            if n % 100 == 0 or n == len(assets):
                print(f'ASSETS: {n}/{len(assets)}; {asset_bytes / 1048576:.1f} MiB; failures={len(failed)}', flush=True)
    if failed:
        missing_assets = dict(sorted(missing_assets.items()))
        write_json(stage / 'missing-assets.json', list(missing_assets.values()))
        if not args.allow_missing_assets:
            raise ValueError(f'{len(failed)} assets failed; no complete inventory generated')
        for key in missing_assets:
            del assets[key]

    page_map = {page_key(p['source_path']): p['local_path'] for p in pages}
    unresolved_media = []
    internal_links = 0
    media_links = 0
    inventory_pages = []
    for page in pages:
        props = documents[page['source_url']]
        context = props['context']
        current = PurePosixPath(page['local_path'])

        def rewrite(raw, image=False):
            nonlocal internal_links, media_links
            clean = html.unescape(raw.strip('<>'))
            parsed = urlsplit(clean)
            if not clean or clean.startswith(('#', 'mailto:', 'data:')):
                return raw
            if parsed.netloc and parsed.netloc not in ('www.palantir.com', 'palantir.com'):
                return raw
            asset = asset_key(clean, context)
            asset = asset_aliases.get(asset, asset)
            if not asset:
                suffix = unquote(parsed.path).split('/')[-1]
                matches = [p for p in props.get('docAssetMetadata', {}) if unquote(p).endswith('/' + suffix)]
                if len(matches) == 1:
                    asset = matches[0]
            if asset:
                if asset in missing_assets:
                    media_links += 1
                    return missing_assets[asset]['url']
                if asset not in assets:
                    unresolved_media.append({'page': page['source_url'], 'target': clean, 'mapped': asset})
                    return urljoin(ORIGIN, asset)
                destination = PurePosixPath('assets') / assets[asset]['local_path']
                relative = os.path.relpath(str(destination), str(PurePosixPath('docs') / current.parent))
                media_links += 1
                return quote(relative, safe='/.-_~') + (('#' + parsed.fragment) if parsed.fragment else '')
            absolute = urljoin(page['source_url'], clean)
            key = page_key(urlsplit(absolute).path)
            if key in page_map:
                relative = os.path.relpath(page_map[key], str(current.parent))
                internal_links += 1
                return quote(relative, safe='/.-_~') + (('#' + parsed.fragment) if parsed.fragment else '')
            if image or re.search(r'(?:^|/)media/|\.(?:png|jpg|jpeg|gif|svg|webp|mp4|webm|pdf)$', parsed.path, re.I):
                unresolved_media.append({'page': page['source_url'], 'target': clean})
            return absolute

        def prose(text):
            missing_urls = {item['url'] for item in missing_assets.values()}

            def missing_img(match):
                tag = match[0]
                source = re.search(r'\bsrc=["\']([^"\']+)["\']', tag)
                if not source:
                    return tag
                target = rewrite(source[1], True)
                if target not in missing_urls:
                    return tag
                alt = re.search(r'\balt=["\']([^"\']*)["\']', tag)
                return '[官方图片已失效：' + (alt[1] if alt else '配图') + '](' + target + ')'

            text = re.sub(r'<img\b[^>]*>', missing_img, text, flags=re.I)

            def markdown_link(match):
                target = rewrite(match[2], match[1].startswith('!'))
                prefix = match[1]
                if target in missing_urls and prefix.startswith('!['):
                    prefix = '[官方图片已失效：' + prefix[2:]
                return prefix + target + match[3]

            text = LINK.sub(markdown_link, text)
            text = ATTR.sub(lambda m: m[1] + rewrite(m[2], m[1].startswith(('src', 'poster'))) + m[3], text)
            return REF.sub(lambda m: m[1] + rewrite(m[2]), text)

        parts = FENCES.split(props['markdown'])
        converted = ''.join(part if n % 2 else prose(part) for n, part in enumerate(parts))
        missing_here = [record for record in missing_assets.values() if record['url'] in converted]
        if missing_here:
            note = ('\n\n> 配图缺失说明：本页有 ' + str(len(missing_here))
                    + ' 个官方图片地址在抓取及重试时失效（返回 HTML 错误页）。'
                    + '下列地址保留用于溯源，未替换成其他版本的图片。\n\n')
            note += '\n'.join('- 官方图片已失效：<' + record['url'] + '>' for record in missing_here)
            converted += note + '\n'
        converted = unicodedata.normalize('NFC', converted.replace('\r\n', '\n').replace('\r', '\n'))
        converted = '\n'.join(line.rstrip() for line in converted.split('\n')).rstrip() + '\n'
        destination = stage / 'docs' / current
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(converted, encoding='utf-8')
        headings = re.findall(r'^#{2,4}\s+(.+)$', converted, re.M)
        inventory_pages.append({
            **{k: page[k] for k in ('title', 'source_url', 'source_path', 'local_path')},
            'summary': '；'.join(headings[:4])[:200],
            'keywords': [*page['groups'], context, props['pageId']],
        })
    if unresolved_media:
        write_json(stage / 'unresolved-media.json', unresolved_media)
        raise ValueError(f'{len(unresolved_media)} unresolved media references; inspect before building')
    inventory = {
        'schema_version': 1, 'source_root': ROOT,
        'coverage': {'discovered': len(pages), 'captured': len(pages), 'failed': [], 'excluded': [
            {'url': ORIGIN + '/docs/foundry/ontology/overview/', 'reason': 'Other language editions are outside the Chinese snapshot'},
            {'url': ORIGIN + '/docs/foundry/api-reference/', 'reason': 'Separate API reference; outside the Ontology sidebar navigation'},
        ]},
        'pages': inventory_pages, 'assets': [assets[key] for key in sorted(assets)],
    }
    write_json(stage / 'inventory.json', inventory)
    write_json(stage / 'capture-report.json', {
        'navigation_pages': len(pages), 'sitemap_verified': len(pages),
        'assets_discovered': len(assets) + len(missing_assets),
        'assets_captured': len(assets), 'asset_bytes': asset_bytes,
        'missing_assets': list(missing_assets.values()),
        'media_complete': not missing_assets,
        'rewritten_document_links': internal_links, 'rewritten_media_links': media_links,
        'source_format': 'Official pageProps.markdown from server-rendered __NEXT_DATA__',
        'rendered_image_urls_verified': len(set().union(*(set(p['_rendered_media_paths']) for p in documents.values()))),
        'locale_specific_image_aliases': asset_aliases,
    })
    status = 'COMPLETE' if not missing_assets else 'DOCUMENTS_COMPLETE_MEDIA_PARTIAL'
    print(f'{status}: {len(pages)} pages, {len(assets)} assets, {len(missing_assets)} missing media; '
          f'{internal_links} local document links', flush=True)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        raise SystemExit(2)

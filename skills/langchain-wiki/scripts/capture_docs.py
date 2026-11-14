#!/usr/bin/env python3
"""Capture LangChain Python official Markdown and navigation into Baize staging.

Only Python's LangChain subtree, its shared Retrieval page and linked changelog
are included. No API keys, browser sessions or third-party packages are used.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import html
import json
from pathlib import Path
import posixpath
import re
import sys
import unicodedata
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit, quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ORIGIN = 'https://docs.langchain.com'
ROOT = ORIGIN + '/oss/python/langchain/overview'
INDEX = ORIGIN + '/_llms/agent-development-lifecycle/build/python.txt'
REPO = 'https://raw.githubusercontent.com/langchain-ai/docs'
PREFIX = '/oss/python/langchain/'
SHARED = '/oss/python/deepagents/retrieval'
CHANGELOG = '/oss/python/releases/changelog'
LINK = re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)([^)\n]*\))')
IMAGE = re.compile(r'!\[[^\]\n]*\]\(([^\s)]+)')
HTML_IMAGE = re.compile(r'<(?:img|source)\b[^>]*?\bsrc=["\']([^"\']+)["\']', re.I)


def fetch(url: str, cache: Path | None = None) -> tuple[bytes, str]:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.username or parsed.password:
        raise ValueError(f'Expected public HTTPS URL: {url}')
    if re.search(r'(?i)(token|signature|credential|secret|expires)=', parsed.query):
        raise ValueError('Credential-bearing or signed URLs cannot be captured')
    key = hashlib.sha256(url.encode()).hexdigest()
    if cache and (cache / (key + '.json')).exists():
        return (cache / key).read_bytes(), json.loads((cache / (key + '.json')).read_text())['kind']
    for attempt in range(3):
        try:
            req = Request(url, headers={'User-Agent': 'LangChain-Wiki/1.0 (public offline documentation)'})
            with urlopen(req, timeout=40) as response:
                data, kind = response.read(), response.headers.get('Content-Type', '')
            if cache:
                cache.mkdir(parents=True, exist_ok=True)
                (cache / key).write_bytes(data)
                (cache / (key + '.json')).write_text(json.dumps({'kind': kind}))
            return data, kind
        except Exception:
            if attempt == 2:
                raise
    raise RuntimeError('Unreachable retry state')


def canonical(path: str) -> str:
    path = path.removesuffix('.md').rstrip('/')
    path = path.removesuffix('/index')
    if path == PREFIX + 'retrieval':
        return SHARED
    if path == PREFIX + 'changelog-py':
        return CHANGELOG
    return path


def clean_url(raw: str) -> str:
    # Mintlify Markdown escapes ampersands in optimized image query strings.
    return html.unescape(raw).replace('\\&', '&')


def safe_name(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', unicodedata.normalize('NFC', html.unescape(value)))
    value = value.strip(' .')
    if not value or value in {'.', '..'}:
        raise ValueError('Unsafe page or group title')
    return value


def outside_code(text: str, transform) -> str:
    result, chunk = [], []
    fence = None
    for line in text.splitlines(keepends=True):
        # Markdown exports can contain code fences inside quoted accordions.
        marker = re.match(r'^(?:> ?)*\s*(`{3,}|~{3,})(.*)$', line)
        if fence is None and marker:
            result.append(transform(''.join(chunk)))
            chunk = []
            fence = (marker[1][0], len(marker[1]))
            result.append(line)
        elif fence:
            result.append(line)
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
        else:
            chunk.append(line)
    if fence:
        raise ValueError('Unclosed Markdown code fence')
    result.append(transform(''.join(chunk)))
    return ''.join(result)


def discover(cache: Path | None) -> tuple[list[dict], dict, list[dict]]:
    tree = json.loads(fetch('https://api.github.com/repos/langchain-ai/docs/git/trees/main?recursive=1', cache)[0])
    if tree.get('truncated'):
        raise ValueError('Official source tree is truncated')
    revision = tree['sha']
    navigation = json.loads(fetch(f'{REPO}/{revision}/src/docs.json', cache)[0])
    index = fetch(INDEX, cache)[0].decode()
    sitemap = ET.fromstring(fetch(ORIGIN + '/sitemap.xml', cache)[0])
    pages: dict[str, dict] = {}
    def add(path, groups, origin):
        path = canonical(path)
        if path not in pages:
            pages[path] = {'source_path': path, 'source_url': ORIGIN + path, 'groups': groups, 'discovered_by': []}
        if origin not in pages[path]['discovered_by']:
            pages[path]['discovered_by'].append(origin)
    def walk(obj, labels=()):
        if isinstance(obj, dict):
            extra = tuple(obj[k] for k in ('language', 'dropdown', 'tab', 'group') if isinstance(obj.get(k), str))
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    walk(value, labels + extra)
        elif isinstance(obj, list):
            for value in obj:
                if isinstance(value, str) and value.startswith('oss/python/'):
                    if value.startswith('oss/python/langchain/') and not value.endswith('/academy'):
                        if 'Python' in labels and ('LangChain' in labels or 'Learn' in labels):
                            offset = labels.index('LangChain') if 'LangChain' in labels and 'Learn' not in labels else labels.index('Learn') - 1
                            groups = list(labels[offset+1:])
                            add('/' + value, groups or ['Overview'], 'navigation')
                    elif value == SHARED.lstrip('/') and 'LangChain' in labels:
                        add('/' + value, ['Advanced usage'], 'navigation')
                else:
                    walk(value, labels)
    walk(navigation)
    for node in sitemap.iter():
        if node.tag.endswith('}loc') and node.text:
            path = urlsplit(node.text).path
            if path.startswith(PREFIX):
                add(path, ['Additional documentation'], 'sitemap')
    for match in re.finditer(r'\[[^\]]+\]\((https://docs\.langchain\.com/[^)]+)\)', index):
        path = urlsplit(match[1]).path
        if path.startswith(PREFIX):
            add(path, ['Additional documentation'], 'python-index')
    excluded = [{'url': ORIGIN + PREFIX + 'academy', 'reason': 'External course catalog (academy.langchain.com), not a documentation page'},
                {'url': ORIGIN + '/oss/javascript', 'reason': 'Different language / SDK'},
                {'url': ORIGIN + '/oss/python/integrations', 'reason': 'Separate provider integration catalog outside the LangChain subtree'},
                {'url': ORIGIN + '/oss/python/langgraph', 'reason': 'Separate LangGraph documentation'},
                {'url': ORIGIN + '/oss/python/deepagents', 'reason': 'Separate Deep Agents documentation, except the Retrieval page shared in LangChain navigation'},
                {'url': ORIGIN + '/langsmith', 'reason': 'Separate LangSmith product documentation'},
                {'url': 'https://reference.langchain.com/python/', 'reason': 'Separate generated API reference'}]
    source_paths = []
    for item in tree['tree']:
        path = item['path']
        if path.startswith('src/oss/langchain/') and path.endswith('.mdx'):
            stem = path.removeprefix('src/oss/langchain/').removesuffix('.mdx')
            if stem in {'academy', 'changelog-js'}:
                continue
            source_paths.append(canonical(PREFIX + stem))
            groups = ['Error reference'] if stem.startswith('errors/') else ['Additional documentation']
            add(PREFIX + stem, groups, 'official-source')
    # Every deployed LangChain page and every source file in scope must be represented.
    if not pages or not set(source_paths) <= pages.keys():
        raise ValueError('Incomplete source inventory')
    audit = {'source_revision': revision, 'source_file_count': len(source_paths),
             'navigation_count': sum('navigation' in p['discovered_by'] for p in pages.values()),
             'sitemap_count': sum('sitemap' in p['discovered_by'] for p in pages.values()),
             'python_index_count': sum('python-index' in p['discovered_by'] for p in pages.values()),
             'pages': sorted(pages.values(), key=lambda p: p['source_path'])}
    return audit['pages'], audit, excluded


def capture(page: dict, cache: Path | None) -> tuple[dict, str]:
    data, kind = fetch(page['source_url'] + '.md', cache)
    if 'text/markdown' not in kind:
        raise ValueError(f'Expected Markdown, got {kind}: {page["source_url"]}')
    text = data.decode('utf-8')
    text = re.sub(r'\A> ## Documentation Index\n(?:>[^\n]*\n)+\n', '', text)
    # Normalize upstream dummy credentials so repository secret scanners can
    # distinguish placeholders. Never substitute values supplied by the user.
    text = re.sub(
        r"(?i)(\b(?:[A-Z_]*API_KEY|api_key)\s*=\s*[\"'])(?:your-api-key|YOUR_KEY_HERE|your-langsmith-api-key|YOUR_API_KEY|your_langsmith_api_key)([\"'])",
        r"\1<API_KEY>\2", text,
    )
    title = re.search(r'^# (.+)$', text, re.M)
    if not title or len(text.strip()) < 100:
        raise ValueError('Missing page title or body')
    title = html.unescape(title[1]).strip()
    summary = re.search(r'^> ([^\n]+)', text, re.M)
    groups = page['groups']
    path = '/'.join([*(safe_name(x) for x in groups), safe_name(title) + '.md'])
    page = {**page, 'title': title, 'local_path': path,
            'summary': summary[1] if summary else title,
            'keywords': [*groups, title, page['source_path'].rsplit('/', 1)[-1]]}
    # Remove volatile visual theme metadata without modifying code examples.
    text = re.sub(r'^(\s*(?:> ?)*\s*`{3,}[^\n]*?) theme=\{[^\n]+\}(\s*)$', r'\1\2', text, flags=re.M)
    return page, text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir', required=True, type=Path)
    parser.add_argument('--cache-dir', type=Path, help='Optional HTTP cache in temporary storage; use a fresh cache on updates')
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 12:
        parser.error('--workers must be between 1 and 12')
    staging = args.staging_dir
    if (staging / 'inventory.json').exists() or (staging / 'docs').exists():
        parser.error('Use a fresh staging directory')
    staging.mkdir(parents=True, exist_ok=True)
    pages, audit, excluded = discover(args.cache_dir)
    print(f'DISCOVERED {len(pages)} pages; navigation={audit["navigation_count"]}, sitemap={audit["sitemap_count"]}, official-source={audit["source_file_count"]}', flush=True)
    (staging / 'discovery.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    captured, failed = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(capture, page, args.cache_dir): page for page in pages}
        for future in as_completed(futures):
            page = futures[future]
            try:
                captured.append(future.result())
            except Exception as exc:
                failed.append({'url': page['source_url'], 'error': type(exc).__name__, 'detail': str(exc)})
                print(f'FAILED {page["source_url"]}: {exc}', flush=True)
            if (len(captured) + len(failed)) % 10 == 0:
                print(f'CAPTURED {len(captured)}/{len(pages)}; failed={len(failed)}', flush=True)
    if len({p['local_path'].casefold() for p, _ in captured}) != len(captured):
        raise ValueError('Duplicate local document path')
    path_map = {p['source_path']: p['local_path'] for p, _ in captured}
    assets = set()
    for page, text in captured:
        def find_assets(prose):
            assets.update(urljoin(page['source_url'], clean_url(url)) for url in IMAGE.findall(prose))
            assets.update(urljoin(page['source_url'], clean_url(url)) for url in HTML_IMAGE.findall(prose))
            return prose
        outside_code(text, find_assets)
    asset_records = []
    def get_asset(url):
        original_url = url
        parsed = urlsplit(url)
        if parsed.netloc == 'mintcdn.com':
            # Prefer the MIT-licensed official original; omit CDN optimization signatures.
            source_path = 'src/' + parsed.path.split('/', 3)[3]
            url = f'{REPO}/main/{source_path}'
            fetch_url = f'{REPO}/{audit["source_revision"]}/{source_path}'
        else:
            fetch_url = url
        data, kind = fetch(fetch_url, args.cache_dir)
        if not kind.startswith('image/'):
            raise ValueError(f'Expected image, got {kind}')
        extension = {'image/svg+xml': '.svg', 'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp', 'image/gif': '.gif', 'image/avif': '.avif'}.get(kind.split(';')[0])
        if extension is None:
            raise ValueError(f'Unsupported image type: {kind}')
        name = safe_name(Path(unquote(urlsplit(url).path)).stem)[:70]
        local = name + '-' + hashlib.sha256(url.encode()).hexdigest()[:12] + extension
        dest = staging / 'assets' / local
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return {'source_url': url, 'local_path': local, '_original_url': original_url}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(get_asset, url): url for url in sorted(assets)}
        for future in as_completed(futures):
            try:
                asset_records.append(future.result())
            except Exception as exc:
                failed.append({'url': futures[future], 'error': type(exc).__name__, 'detail': str(exc)})
                print(f'ASSET FAILED {futures[future]}: {exc}', flush=True)
    asset_map = {a.pop('_original_url'): a['local_path'] for a in asset_records}
    for page, text in captured:
        parent = posixpath.dirname(page['local_path'])
        def local_url(raw, image=False):
            absolute = urljoin(page['source_url'], clean_url(raw))
            parsed = urlsplit(absolute)
            if absolute in asset_map:
                target = posixpath.relpath('../assets/' + asset_map[absolute], parent)
                return quote(target, safe='/.-_')
            if not image and parsed.netloc == 'docs.langchain.com' and canonical(parsed.path) in path_map:
                if raw.startswith('#'):
                    return raw
                target = posixpath.relpath(path_map[canonical(parsed.path)], parent)
                return quote(target, safe='/.-_') + ('#' + parsed.fragment if parsed.fragment else '')
            if raw.startswith(('/', './', '../')):
                return absolute
            return raw
        def rewrite(prose):
            prose = LINK.sub(lambda m: m[1] + local_url(m[2], m[1].startswith('!')) + m[3], prose)
            prose = re.sub(r'(<(?:img|source)\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])', lambda m: m[1] + local_url(m[2], True) + m[3], prose, flags=re.I)
            prose = re.sub(r'(<a\b[^>]*?\bhref=["\'])([^"\']+)(["\'])', lambda m: m[1] + local_url(m[2]) + m[3], prose, flags=re.I)
            return prose
        text = outside_code(text, rewrite)
        target = staging / 'docs' / page['local_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(unicodedata.normalize('NFC', text).rstrip() + '\n')
    # Asset failures also block a complete snapshot, independently of page counts.
    page_failures = [f for f in failed if f['url'] in {p['source_url'] for p in pages}]
    inventory = {'schema_version': 1, 'source_root': ROOT,
                 'coverage': {'discovered': len(pages), 'captured': len(captured), 'failed': page_failures, 'excluded': excluded},
                 'pages': [p for p, _ in sorted(captured, key=lambda item: item[0]['local_path'])],
                 'assets': sorted(asset_records, key=lambda a: a['local_path'])}
    if not failed:
        (staging / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    (staging / 'capture-report.json').write_text(json.dumps({'pages': len(captured), 'assets': len(asset_records), 'failures': failed}, ensure_ascii=False, indent=2) + '\n')
    print(f'RESULT pages={len(captured)}/{len(pages)}, assets={len(asset_records)}/{len(assets)}, failures={len(failed)}', flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)

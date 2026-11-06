#!/usr/bin/env python3
"""Capture the complete English Python LangGraph documentation into Baize staging."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import http.client
import html
import json
from pathlib import Path
import posixpath
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = 'https://docs.langchain.com/'
REPO = 'https://raw.githubusercontent.com/langchain-ai/docs/main/'
PREFIX = 'oss/python/langgraph/'
ROOT = BASE + PREFIX.rstrip('/')
LINK = re.compile(r'(!?\[[^\]\n]*\])\(([^\s]+?)(?:\s+"[^"\n]*")?\)')


def fetch(url: str) -> tuple[bytes, str, str]:
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'LangGraphWikiSkill/1.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read(), response.url, response.headers.get('Content-Type', '')
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException, ConnectionError):
            if attempt == 2:
                raise
    raise AssertionError('unreachable')


def text(url: str) -> str:
    return fetch(url)[0].decode('utf-8')


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def safe(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', value).strip(' .')
    if value in ('', '.', '..'):
        raise ValueError(f'Invalid path component: {value!r}')
    return value


def key(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path.removesuffix('.md').rstrip('/')
    return path.lstrip('/') if parsed.netloc in ('', 'docs.langchain.com') else url


def markdown(page: str) -> tuple[str, str]:
    data, final_url, content_type = fetch(BASE + page + '.md')
    body = data.decode('utf-8')
    if 'text/html' in content_type or body.lstrip().lower().startswith('<!doctype'):
        # Mintlify redirects sometimes discard the .md suffix.
        data, final_url, content_type = fetch(final_url.rstrip('/') + '.md')
        body = data.decode('utf-8')
    if 'text/html' in content_type or not re.search(r'^# .+', body, re.M):
        raise ValueError(f'Not a complete Markdown page: {page}')
    body = re.sub(r'\A> ## Documentation Index\n(?:>[^\n]*\n)+\s*', '', body)
    body = re.sub(r'\n\*\*\*\n\n\[Connect these docs\][\s\S]*\Z', '\n', body)
    # Remove rendering theme metadata, retaining code languages and tab titles.
    body = re.sub(r'^(\s*```[^\n]*?)\s+theme=\{[^\n]*$', r'\1', body, flags=re.M)
    # Keep official credential examples visibly generic for repository scanners.
    placeholder = re.compile(r"""(?i)((?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['"])([^'"\n]{12,})(['"])""")
    body = placeholder.sub(
        lambda m: m[1] + '<API_KEY>' + m[3] if 'your' in m[2].lower() else m[0], body
    )
    return body.strip() + '\n', final_url.removesuffix('.md')


def asset_source(url: str) -> str:
    url = html.unescape(url.replace('\\&', '&'))
    parsed = urllib.parse.urlsplit(url)
    if parsed.netloc == 'mintcdn.com':
        parts = parsed.path.split('/', 3)
        if len(parts) != 4:
            raise ValueError(f'Unknown Mintlify asset path: {parsed.path}')
        return REPO + 'src/' + parts[3]
    if parsed.netloc == 'docs.langchain.com':
        return REPO + 'src' + parsed.path
    if parsed.query:
        raise ValueError(f'Asset requires review of query parameters: {url}')
    return url


def capture(staging: Path, workers: int) -> None:
    if (staging / 'inventory.json').exists():
        raise ValueError('Use a fresh mktemp directory; inventory already exists')
    config = json.loads(text(REPO + 'src/docs.json'))
    tree = json.loads(text('https://api.github.com/repos/langchain-ai/docs/git/trees/main?recursive=1'))
    if tree.get('truncated'):
        raise ValueError('Upstream source tree is truncated')
    sitemap = ET.fromstring(fetch(BASE + 'sitemap.xml')[0])
    index = text(BASE + '_llms/agent-development-lifecycle/build/python.txt')
    tabs = [v for v in walk(config) if v.get('tab') == 'LangGraph'
            and PREFIX + 'overview' in v.get('pages', [])]
    if len(tabs) != 1:
        raise ValueError('Cannot identify a unique Python LangGraph navigation tab')
    groups: dict[str, tuple[str, ...]] = {}

    def navigation(items, group=()):
        for item in items:
            if isinstance(item, str):
                groups.setdefault(item, group)
            elif 'pages' in item:
                navigation(item['pages'], group + (safe(item['group']),))

    navigation(tabs[0]['pages'])
    nav_count = len(groups)
    sitemap_pages = {key(e.text) for e in sitemap.iter() if e.tag.endswith('}loc')
                     and e.text and key(e.text).startswith(PREFIX)}
    index_pages = {key(u) for u in re.findall(r'\]\((https://docs\.langchain\.com/[^)]+)\)', index)
                   if key(u).startswith(PREFIX)}
    source_pages = {PREFIX + x['path'].removeprefix('src/oss/langgraph/').rsplit('.', 1)[0]
                    for x in tree['tree'] if x['type'] == 'blob'
                    and x['path'].startswith('src/oss/langgraph/')
                    and x['path'].endswith(('.md', '.mdx'))}
    excluded = {PREFIX + 'changelog-js'}  # Only the Python changelog belongs to this snapshot.
    for page in sorted((sitemap_pages | index_pages | source_pages) - excluded):
        if page not in groups:
            if '/errors/' in page:
                groups[page] = ('Reference', 'Errors')
            elif page.endswith(('agentic-rag', 'sql-agent')):
                groups[page] = ('Learn', 'Tutorials')
            elif page.endswith('case-studies'):
                groups[page] = ('Learn', 'Additional resources')
            else:
                raise ValueError(f'Unmapped new upstream page: {page}; review navigation first')
    print(json.dumps({'navigation_pages': nav_count, 'sitemap_pages': len(sitemap_pages),
                      'index_pages': len(index_pages), 'source_pages': len(source_pages),
                      'discovered': len(groups)}, ensure_ascii=False), flush=True)
    # All discovery finishes before any document is written.
    captured = {}
    failures = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(markdown, page): page for page in groups}
        for future in as_completed(futures):
            page = futures[future]
            try:
                captured[page] = future.result()
            except Exception as exc:
                failures.append({'url': BASE + page, 'error': str(exc)})
    if failures:
        raise ValueError(json.dumps({'failed': failures}, ensure_ascii=False))
    canonical_urls = [value[1] for value in captured.values()]
    if len(set(canonical_urls)) != len(canonical_urls):
        raise ValueError('Upstream canonical pages overlap; review path mapping before capture')
    paths = {}
    for page in sorted(captured):
        body, _ = captured[page]
        title = html.unescape(re.search(r'^# (.+)$', body, re.M)[1])
        local = '/'.join((*groups[page], safe(title) + '.md'))
        if local in paths.values():
            local = '/'.join((*groups[page], safe(title) + ' (' + safe(page.split('/')[-1]) + ').md'))
        if local in paths.values():
            raise ValueError(f'Duplicate local path: {local}')
        paths[page] = local
    aliases = {page: paths[page] for page in paths}
    # Prefer explicit navigation paths when multiple pages redirect to the same source.
    for page, (_, canonical) in captured.items():
        aliases.setdefault(key(canonical), paths[page])
    redirects = {key(r['source']): r['destination'] for r in config.get('redirects', [])
                 if '*' not in r.get('source', '') and '#' not in r.get('source', '')}
    for old, dest in redirects.items():
        for _ in range(12):
            if key(dest) in aliases:
                aliases[old] = aliases[key(dest)]
                break
            if key(dest) not in redirects:
                break
            dest = redirects[key(dest)]
    asset_urls = set()
    for page, (body, _) in captured.items():
        for match in LINK.finditer(body):
            if match[1].startswith('!'):
                asset_urls.add(asset_source(urllib.parse.urljoin(BASE + page, match[2])))
    assets = []
    asset_paths = {}

    def download_asset(url):
        data, _, content_type = fetch(url)
        if not data or 'text/html' in content_type:
            raise ValueError(f'Empty or HTML asset: {url}')
        basename = safe(urllib.parse.unquote(urllib.parse.urlsplit(url).path.rsplit('/', 1)[-1]))
        local = 'images/' + hashlib.sha256(url.encode()).hexdigest()[:12] + '-' + basename
        return url, local, data

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for url, local, data in pool.map(download_asset, sorted(asset_urls)):
            target = staging / 'assets' / local
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            assets.append({'source_url': url, 'local_path': local})
            asset_paths[url] = local
    pages = []
    for page in sorted(captured):
        body, canonical = captured[page]
        local = paths[page]

        def replace(match):
            label, href = match[1], match[2]
            absolute = urllib.parse.urljoin(BASE + page, html.unescape(href.replace('\\&', '&')))
            parsed = urllib.parse.urlsplit(absolute)
            if label.startswith('!'):
                destination = '../assets/' + asset_paths[asset_source(absolute)]
                relative = posixpath.relpath(destination, posixpath.dirname(local) or '.')
                return label + '(' + urllib.parse.quote(relative, safe='/') + ')'
            if href.startswith('#'):
                return match[0]
            destination = aliases.get(key(absolute))
            if destination:
                relative = posixpath.relpath(destination, posixpath.dirname(local) or '.')
                return label + '(' + urllib.parse.quote(relative, safe='/') + ('#' + parsed.fragment if parsed.fragment else '') + ')'
            return label + '(' + absolute + ')'

        # Process prose only: code examples retain languages, with theme metadata and credential placeholders normalized.
        converted = []
        fence = None
        for line in body.splitlines(keepends=True):
            marker = re.match(r'^\s*(`{3,}|~{3,})', line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                    fence = None
                converted.append(line)
            else:
                converted.append(LINK.sub(replace, line) if fence is None else line)
        body = ''.join(converted)
        target = staging / 'docs' / local
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')
        title = html.unescape(re.search(r'^# (.+)$', body, re.M)[1])
        summary = next((l[2:].strip() for l in body.splitlines()[1:] if l.startswith('> ')), '')
        pages.append({'title': title, 'source_url': BASE + page,
                      'source_path': '/' + page, 'local_path': local,
                      'summary': summary[:350],
                      'keywords': list(dict.fromkeys([*groups[page], *page.split('/')[-1].split('-')]))})
    inventory = {'schema_version': 1, 'source_root': ROOT,
                 'coverage': {'discovered': len(groups), 'captured': len(pages), 'failed': [],
                              'excluded': [{'url': BASE + PREFIX + 'changelog-js', 'reason': 'JavaScript-only source variant'},
                                           {'url': BASE + 'oss/javascript/langgraph/overview', 'reason': 'Different SDK language'},
                                           {'url': 'https://reference.langchain.com/python/langgraph/', 'reason': 'Separate API reference site outside the requested documentation scope'}]},
                 'pages': pages, 'assets': assets}
    (staging / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    provenance = {'repository': 'https://github.com/langchain-ai/docs', 'source_tree_sha': tree['sha'],
                  'navigation_pages': nav_count, 'sitemap_pages': len(sitemap_pages),
                  'index_pages': len(index_pages), 'source_pages': len(source_pages),
                  'documents': len(pages), 'assets': len(assets),
                  'canonical_redirects': {BASE + p: c for p, (_, c) in captured.items() if BASE + p != c}}
    (staging / 'capture-report.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(provenance, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be between 1 and 8')
    capture(args.staging_dir.resolve(), args.workers)

#!/usr/bin/env python3
"""Capture the complete English Python LangSmith documentation into Baize staging."""
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
PREFIX = 'langsmith/'
ROOT = BASE + PREFIX.rstrip('/')
LINK = re.compile(r'(!?\[[^\]\n]*\])\(([^\s]+?)(?:\s+"[^"\n]*")?\)')


def fetch(url: str) -> tuple[bytes, str, str]:
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'LangSmithWikiSkill/1.0'})
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


def normalize_credentials(body: str) -> str:
    """Keep upstream example credentials clearly generic and scanner safe."""
    literal = re.compile(r"""(?i)((?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['"])([^'"]{12,})(['"])""")
    body = literal.sub(lambda m: m[1] + '<SECRET>' + m[3], body)
    body = re.sub(r'(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}', '<API_KEY>', body)
    body = re.sub(r'AKIA[0-9A-Z]{16}', '<AWS_KEY>', body)
    body = re.sub(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', '<PRIVATE_KEY_HEADER>', body)
    body = re.sub(r'-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', '<PRIVATE_KEY_FOOTER>', body)
    return body


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
    return normalize_credentials(body).strip() + '\n', final_url.removesuffix('.md')


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
    groups = {}
    nav_occurrences = []
    def navigation(value, group=()):
        if isinstance(value, str):
            if value.startswith(PREFIX):
                groups.setdefault(value, group)
                nav_occurrences.append((value, group))
        elif isinstance(value, list):
            for child in value:
                navigation(child, group)
        elif isinstance(value, dict):
            label = next((value[k] for k in ('product', 'item', 'dropdown', 'tab', 'group') if k in value), None)
            for k, child in value.items():
                if k in ('pages', 'products', 'menu', 'dropdowns', 'tabs', 'groups'):
                    navigation(child, group + ((safe(label),) if label and label not in ('AGENT DEVELOPMENT LIFECYCLE', 'PRODUCTS AND SETUP') else ()))
    navigation(config['navigation'])
    nav_count = len(groups)
    evaluation_nav = sorted({p for p, g in nav_occurrences if g and g[0] == 'Test'})
    sitemap_pages = {key(e.text) for e in sitemap.iter() if e.tag.endswith('}loc')
                     and e.text and key(e.text).startswith(PREFIX)}
    # Traverse the official hierarchical llms indexes, retaining their heading groups.
    index_groups = {}
    visited = set()
    def index(url, route=()):
        if url in visited:
            return
        visited.add(url)
        headings = {}
        children = []
        for line in text(url).splitlines():
            h = re.match(r'^(#{1,6}) (.+)', line)
            if h:
                level = len(h[1])
                headings = {k: v for k, v in headings.items() if k < level}
                label = h[2].removeprefix('Docs by LangChain: ')
                if level > 1 and label not in ('AGENT DEVELOPMENT LIFECYCLE', 'PRODUCTS AND SETUP', 'Indexes'):
                    headings[level] = safe(label)
            m = re.search(r'\]\((https://docs\.langchain\.com/[^)]+)\)', line)
            if not m:
                continue
            href = m[1]
            if '/_llms/' in href and href.endswith('.txt'):
                label = re.search(r'\[([^]]+)\]', line)[1]
                breadcrumb = re.sub(r' \(\d+ pages\)$', '', label).split(' / ')
                children.append((href, tuple(safe(x) for x in breadcrumb if x not in ('AGENT DEVELOPMENT LIFECYCLE', 'PRODUCTS AND SETUP'))))
            elif key(href).startswith(PREFIX):
                group = list(route)
                for label in headings.values():
                    if not group or group[-1] != label:
                        group.append(label)
                index_groups.setdefault(key(href), tuple(group))
        for child, breadcrumb in children:
            index(child, breadcrumb)
    index(BASE + 'llms.txt')
    index_pages = set(index_groups)
    source_pages = {x['path'][4:].rsplit('.', 1)[0] for x in tree['tree']
                    if x['path'].startswith('src/langsmith/') and x['path'].endswith(('.md', '.mdx'))}
    for page in sorted(sitemap_pages | index_pages):
        if page not in groups:
            groups[page] = index_groups.get(page) or (('Reference', 'LangSmith REST API', safe(page.split('/')[2])) if page.startswith('langsmith/smith-api/')
                else ('Reference', 'Agent Server API', safe(page.split('/')[2])) if page.startswith('langsmith/agent-server-api/')
                else ('Additional documentation',))
    print(json.dumps({'navigation_pages': nav_count, 'evaluation_navigation_pages': len(evaluation_nav),
                      'sitemap_pages': len(sitemap_pages), 'index_pages': len(index_pages),
                      'discovered_urls': len(groups)}, ensure_ascii=False), flush=True)
    captured = {}
    failures = []
    cache = staging / '.capture-cache'
    cache.mkdir(exist_ok=True)
    external_navigation = {}
    previous_failures = {key(x['url']) for x in json.loads((staging / 'failures.json').read_text())} if (staging / 'failures.json').exists() else set()
    def source_stub(page):
        source_page = page
        if source_page not in source_pages:
            source_page = source_page.replace('/python/', '/').replace('/javascript/', '/')
        source = text(REPO + 'src/' + source_page + '.mdx')
        frontmatter = source.split('---', 2)[1] if source.startswith('---') else ''
        match = re.search(r'^url:\s*["\']?([^"\'\n]+)', frontmatter, re.M)
        if not match:
            raise ValueError(f'No upstream redirect stub for failed page: {page}')
        destination = match[1].strip()
        if urllib.parse.urlsplit(destination).netloc == 'docs.langchain.com':
            return markdown(key(destination))
        return None, destination
    def cached_markdown(page):
        path = cache / (hashlib.sha256(page.encode()).hexdigest() + '.json')
        if path.exists():
            body, canonical = json.loads(path.read_text())
            return normalize_credentials(body) if body is not None else None, canonical
        if page in previous_failures:
            value = source_stub(page)
        else:
            try:
                value = markdown(page)
            except (ValueError, urllib.error.URLError, TimeoutError, http.client.HTTPException, ConnectionError):
                value = source_stub(page)
        path.write_text(json.dumps(value, ensure_ascii=False))
        return value
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(cached_markdown, page): page for page in groups}
        for n, future in enumerate(as_completed(futures), 1):
            page = futures[future]
            try:
                value = future.result()
                if value[0] is None:
                    external_navigation[page] = value[1]
                else:
                    captured[page] = value
            except Exception as exc:
                failures.append({'url': BASE + page, 'error': str(exc)})
            if n % 100 == 0:
                print(f'Pages: {n}/{len(groups)}; failures: {len(failures)}', flush=True)
    if failures:
        (staging / 'failures.json').write_text(json.dumps(failures, indent=2))
        raise ValueError(json.dumps({'failed': failures}, ensure_ascii=False))
    # Navigation aliases and redirect stubs are one canonical document, not extra pages.
    by_canonical = {}
    redirect_aliases = {}
    for page in sorted(captured, key=lambda p: (p not in evaluation_nav, p not in dict(nav_occurrences), p)):
        canonical = key(captured[page][1])
        if canonical in by_canonical:
            redirect_aliases[page] = by_canonical[canonical]
        else:
            by_canonical[canonical] = page
    for page in redirect_aliases:
        del captured[page]
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
    for old, destination in redirect_aliases.items():
        aliases[old] = paths[destination]
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
        cache_path = cache / ('asset-' + hashlib.sha256(url.encode()).hexdigest())
        if cache_path.exists():
            data, content_type = cache_path.read_bytes(), ''
        else:
            data, _, content_type = fetch(url)
            cache_path.write_bytes(data)
        if not data or 'text/html' in content_type:
            raise ValueError(f'Empty or HTML asset: {url}')
        if urllib.parse.urlsplit(url).path.lower().endswith('.svg'):
            data = re.sub(rb'(?m)[ \t]+$', b'', data)
        basename = safe(urllib.parse.unquote(urllib.parse.urlsplit(url).path.rsplit('/', 1)[-1]))
        local = 'images/' + hashlib.sha256(url.encode()).hexdigest()[:12] + '-' + basename
        return url, local, data

    with ThreadPoolExecutor(max_workers=workers) as pool:
        print(f'Downloading {len(asset_urls)} assets', flush=True)
        for n, (url, local, data) in enumerate(pool.map(download_asset, sorted(asset_urls)), 1):
            if n % 100 == 0:
                print(f'Assets: {n}/{len(asset_urls)}', flush=True)
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
                 'coverage': {'discovered': len(pages), 'captured': len(pages), 'failed': [],
                              'excluded': [{'url': 'https://reference.langchain.com/', 'reason': 'Separate SDK API reference site; LangSmith REST API pages on docs.langchain.com are included'}] + [{'url': BASE + p, 'destination': u, 'reason': 'External-only navigation shortcut, no LangSmith document body'} for p, u in sorted(external_navigation.items())]},
                 'pages': pages, 'assets': assets}
    (staging / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    provenance = {'repository': 'https://github.com/langchain-ai/docs', 'source_tree_sha': tree['sha'],
                  'navigation_pages': nav_count, 'sitemap_pages': len(sitemap_pages),
                  'index_pages': len(index_pages), 'source_pages': len(source_pages),
                  'documents': len(pages), 'assets': len(assets),
                  'discovered_urls': len(groups),
                  'external_navigation': external_navigation,
                  'evaluation_navigation': evaluation_nav,
                  'evaluation_navigation_covered': len([p for p in evaluation_nav if p in aliases]),
                  'redirect_aliases': redirect_aliases,
                  'source_only_not_published': sorted(source_pages - set(groups)),
                  'index_urls': sorted(visited),
                  'canonical_redirects': {BASE + p: c for p, (_, c) in captured.items() if BASE + p != c}}
    (staging / 'capture-report.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'documents': len(pages), 'assets': len(assets), 'evaluation_covered': provenance['evaluation_navigation_covered']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be between 1 and 8')
    capture(args.staging_dir.resolve(), args.workers)

#!/usr/bin/env python3
"""Capture the official public TokenDance Markdown corpus into a new staging directory.

Python 3.10+ standard library only. Uses HTTPS_PROXY when configured.
No account, credentials or model API calls are needed.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = 'https://tokendance.space'

def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=40) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise

def safe(value):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', value).strip(' .')

def capture(staging):
    if staging.exists() and any(staging.iterdir()):
        raise ValueError('Staging must be empty; existing content will not be overwritten')
    staging.mkdir(parents=True, exist_ok=True)
    index = fetch(ROOT + '/llms.txt').decode()
    full = fetch(ROOT + '/llms-full.txt').decode()
    pages, headings = {}, {}
    in_docs = False
    for line in index.splitlines():
        if line == '## Documentation':
            in_docs = True
            continue
        if not in_docs:
            continue
        heading = re.match(r'^(#{3,5}) (.+)$', line)
        if heading:
            level = len(heading[1])
            headings = {k:v for k,v in headings.items() if k < level}
            headings[level] = safe(heading[2])
        link = re.match(r'^- \[(.+?)\]\((https://tokendance\.space/docs/[^)]+\.md)\): (.*)$', line)
        if link:
            title, url, summary = link.groups()
            path = '/'.join([*headings.values(), safe(title)+'.md'])
            if url in pages or any(p['local_path']==path for p in pages.values()):
                raise ValueError('Duplicate URL or local path')
            pages[url] = dict(title=title, source_url=url, source_path=urllib.parse.urlsplit(url).path,
                              local_path=path, summary=summary)
    bundled = set(re.findall(r'^Source: (https://tokendance\.space/docs/\S+\.md)$', full, re.M))
    if not pages or set(pages) != bundled:
        raise ValueError('Index and full export disagree; stop and inspect navigation')
    # The browser registry includes hidden draft entries. Only visible public docs belong here.
    html = fetch(ROOT + '/docs/quickstart').decode()
    script = re.search(r'<script[^>]+type="module"[^>]+src="([^"]+)"', html)
    if not script:
        raise ValueError('Cannot locate browser navigation registry')
    js = fetch(urllib.parse.urljoin(ROOT, script[1])).decode()
    records = re.findall(r'\{slug:"([^"]+)",path:"/src/docs/([^}]+)\}', js)
    visible = {ROOT+'/docs/'+slug+'.md' for slug, record in records if 'hidden:!0' not in record}
    hidden = {ROOT+'/docs/'+slug+'.md' for slug, record in records if 'hidden:!0' in record}
    if visible != set(pages):
        raise ValueError('Visible browser registry and Markdown index disagree')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        bodies = dict(zip(pages, pool.map(lambda u: fetch(u).decode(), pages)))
    mapping = {urllib.parse.urlsplit(u).path:p['local_path'] for u,p in pages.items()}
    images = sorted({urllib.parse.urljoin(ROOT, url) for body in bodies.values() for url in (re.findall(r'!\[[^\]]*\]\((https://[^)]+)\)', body) + re.findall(r'<img[^>]+src="([^"]+)"', body))})
    asset_paths = {}
    for url in images:
        parsed = urllib.parse.urlsplit(url)
        if parsed.query or parsed.hostname not in {'watcha.tos-cn-beijing.volces.com', 'tos.watcha.cn', 'tokendance.space'}:
            raise ValueError('Unexpected asset host or signed URL; inspect before capturing')
        relative = Path(parsed.hostname) / urllib.parse.unquote(parsed.path.lstrip('/'))
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe asset path')
        asset_paths[url] = (Path(urllib.parse.unquote(parsed.path.lstrip('/'))).as_posix()
                            if parsed.hostname == 'watcha.tos-cn-beijing.volces.com' else relative.as_posix())
    def save_asset(url):
        dest = staging/'assets'/asset_paths[url]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(fetch(url))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(save_asset, images))
    for url, page in pages.items():
        body = bodies[url].replace('YOUR_API_KEY', 'YOUR_KEY')
        if not body.strip() or '<!DOCTYPE html>' in body:
            raise ValueError('Empty or HTML fallback: '+url)
        body = '# '+page['title']+'\n\n'+body.strip()+'\n'
        def rewrite(match):
            target = match[2]
            parsed = urllib.parse.urlsplit(urllib.parse.urljoin(url,target))
            source_path = parsed.path
            if not source_path.endswith('.md'):
                source_path += '.md'
            if parsed.netloc == 'tokendance.space' and source_path in mapping:
                dest = staging/'docs'/mapping[source_path]
            elif target in asset_paths:
                dest = staging/'assets'/asset_paths[target]
            else:
                absolute = urllib.parse.urljoin(url, target) if target.startswith('/') else target
                return match[1]+absolute+match[3]
            relative = os.path.relpath(dest, (staging/'docs'/page['local_path']).parent)
            return match[1]+urllib.parse.quote(relative, safe='/')+('#'+parsed.fragment if parsed.fragment else '')+match[3]
        body = re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))', rewrite, body)
        def rewrite_html(match):
            absolute = urllib.parse.urljoin(ROOT, match[1])
            if absolute not in asset_paths:
                raise ValueError('Uncaptured image: '+absolute)
            relative = os.path.relpath(staging/'assets'/asset_paths[absolute], (staging/'docs'/page['local_path']).parent)
            return 'src="'+urllib.parse.quote(relative, safe='/')+'"'
        body = re.sub(r'src="([^"]+)"', rewrite_html, body)
        dest = staging/'docs'/page['local_path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding='utf-8')
    inventory = dict(schema_version=1, source_root=ROOT+'/docs',
        coverage=dict(discovered=len(pages), captured=len(pages), failed=[],
                      excluded=[dict(url=u,reason='hidden draft in browser registry; absent from public index and export') for u in sorted(hidden)]),
        pages=list(pages.values()), assets=[dict(source_url=u,local_path=p) for u,p in asset_paths.items()])
    (staging/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(pages=len(pages),assets=len(images),hidden_excluded=len(hidden),staging=str(staging)),ensure_ascii=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging-dir',type=Path,required=True)
    args = parser.parse_args()
    capture(args.staging_dir.expanduser().resolve())

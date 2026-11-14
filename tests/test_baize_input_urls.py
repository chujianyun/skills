"""Entry URLs survive build, redirect normalization and incremental updates."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/baize/scripts'
SPEC = importlib.util.spec_from_file_location('baize_sync_urls', SCRIPTS / 'sync_wiki_docs.py')
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


class InputUrlsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.staging = self.root / 'staging'
        (self.staging / 'docs').mkdir(parents=True)
        (self.staging / 'docs/guide.md').write_text('# Guide\n\nInstall instructions.\n')
        self.entry = 'https://example.com/zh/v2/guide?view=full#install'
        self.inventory = {
            'schema_version': 1, 'source_root': 'https://docs.example.com/zh/v2',
            'input_urls': [self.entry, self.entry],
            'coverage': {'discovered': 1, 'captured': 1, 'failed': []},
            'pages': [{'title': 'Guide', 'source_url': 'https://docs.example.com/zh/v2/guide',
                       'local_path': 'guide.md'}],
        }
        self.skill = self.root / 'output/example-wiki'

    def save_inventory(self):
        (self.staging / 'inventory.json').write_text(json.dumps(self.inventory))

    def build(self, *extra):
        self.save_inventory()
        return subprocess.run([
            sys.executable, str(SCRIPTS / 'build_wiki_skill.py'),
            '--staging-dir', str(self.staging), '--target-parent', str(self.skill.parent),
            '--name', 'example-wiki', '--title', 'Example',
            '--source-url', self.inventory['source_root'], '--description', 'Use when asking about Example.',
            *extra,
        ], capture_output=True, text=True)

    def manifest(self):
        return json.loads((self.skill / 'references/wiki-manifest.json').read_text())

    def snapshot(self):
        return {str(p.relative_to(self.skill)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.skill.rglob('*') if p.is_file()}

    def test_build_preserves_original_entry_and_links_update_instructions(self):
        other = 'https://example.com/zh/v2/reference'
        result = self.build('--input-url', other)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.manifest()['wiki']['input_urls'], sorted([self.entry, other]))
        self.assertEqual(self.manifest()['wiki']['source_root'], self.inventory['source_root'])
        self.assertIn(self.entry, (self.skill / 'references/INPUT-URLS.md').read_text())
        self.assertIn('references/INPUT-URLS.md', (self.skill / 'SKILL.md').read_text())
        self.assertIn('INPUT-URLS.md', (self.skill / 'references/UPDATE.md').read_text())

    def test_sync_appends_and_old_inventory_preserves_urls_without_writes(self):
        self.assertEqual(self.build().returncode, 0)
        other = 'https://example.com/zh/v2/api#methods'
        self.inventory['input_urls'] = [other]
        self.save_inventory()
        before = self.snapshot()
        self.assertEqual(sync.sync_skill(self.skill, self.staging, dry_run=True).status, 'DRY_RUN')
        self.assertEqual(before, self.snapshot())
        self.assertEqual(sync.sync_skill(self.skill, self.staging).status, 'CHANGED')
        self.assertEqual(self.manifest()['wiki']['input_urls'], sorted([self.entry, other]))
        self.assertEqual(before['references/docs/guide.md'], self.snapshot()['references/docs/guide.md'])
        del self.inventory['input_urls']
        self.save_inventory()
        before = self.snapshot()
        self.assertEqual(sync.sync_skill(self.skill, self.staging).status, 'UNCHANGED')
        self.assertEqual(before, self.snapshot())

    def test_legacy_manifest_does_not_invent_original_urls(self):
        self.assertEqual(self.build().returncode, 0)
        manifest = self.manifest()
        del manifest['wiki']['input_urls']
        (self.skill / 'references/wiki-manifest.json').write_text(json.dumps(manifest))
        (self.skill / 'references/INPUT-URLS.md').unlink()
        del self.inventory['input_urls']
        self.save_inventory()
        self.assertEqual(sync.sync_skill(self.skill, self.staging).status, 'CHANGED')
        self.assertNotIn('input_urls', self.manifest()['wiki'])
        self.assertIn('未记录原始入口', (self.skill / 'references/INPUT-URLS.md').read_text())
        self.assertEqual(sync.sync_skill(self.skill, self.staging).status, 'UNCHANGED')

    def test_missing_input_and_sensitive_urls_fail_before_creation(self):
        del self.inventory['input_urls']
        self.assertNotEqual(self.build().returncode, 0)
        self.assertFalse(self.skill.exists())
        for url in ['https://user:password@example.com/wiki',
                    'https://example.com/wiki?access_token=private',
                    'https://example.com/wiki?X-Amz-Signature=private']:
            with self.subTest(url_type=url.split('?')[0]):
                self.inventory['input_urls'] = [url]
                self.assertNotEqual(self.build().returncode, 0)
                self.assertFalse(self.skill.exists())

    def test_invalid_update_preserves_existing_skill(self):
        self.assertEqual(self.build().returncode, 0)
        before = self.snapshot()
        for invalid in ['https://example.com/wiki', ['https://example.com/?token=private']]:
            self.inventory['input_urls'] = invalid
            self.save_inventory()
            with self.assertRaises(sync.SyncError):
                sync.sync_skill(self.skill, self.staging)
            self.assertEqual(before, self.snapshot())


if __name__ == '__main__':
    unittest.main()

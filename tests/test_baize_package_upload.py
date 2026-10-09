import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parents[1] / "skills/baize/scripts/package_upload.py"
SPEC = importlib.util.spec_from_file_location("baize_package_upload", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BaizeUploadPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "baize"
        self.source.mkdir()
        self.write("SKILL.md", b"# Baize\n")
        self.output = self.root / "upload.zip"

    def write(self, name, data):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_upload_keeps_business_files_and_excludes_reported_failures(self):
        text = "知识检索\n".encode("utf-8")
        self.write("scripts/sync_wiki_docs.py", text)
        self.write("references/guide.md", text)
        for name in ("assets/icon.png", "scripts/__pycache__/sync_wiki_docs.cpython-314.pyc",
                     "__MACOSX/._baize", "references/._guide.md", ".DS_Store"):
            self.write(name, b"\x00\xff")
        self.write("agents/openai.yaml", b'interface:\n  icon_small: "./assets/icon.png"\n')
        count, skipped = MODULE.package_upload(self.source, self.output)
        self.assertEqual(count, 3)
        self.assertEqual(len(skipped), 6)
        with ZipFile(self.output) as archive:
            self.assertEqual(set(archive.namelist()), {
                "baize/SKILL.md", "baize/scripts/sync_wiki_docs.py", "baize/references/guide.md"})
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.read("baize/references/guide.md"), text)
        self.assertTrue((self.source / "assets/icon.png").exists())

    def test_unexpected_binary_stops_without_creating_package(self):
        for data in (b"\xff", b"text\x00binary"):
            with self.subTest(data=data):
                self.write("references/extra.md", data)
                with self.assertRaises(ValueError):
                    MODULE.package_upload(self.source, self.output)
                self.assertFalse(self.output.exists())

    def test_symlink_stops_without_reading_external_file(self):
        outside = self.root / "outside.txt"
        outside.write_text("outside")
        (self.source / "link.txt").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            MODULE.package_upload(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b"original")
        with self.assertRaises(FileExistsError):
            MODULE.package_upload(self.source, self.output)
        self.assertEqual(self.output.read_bytes(), b"original")

    def test_output_inside_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            MODULE.package_upload(self.source, self.source / "upload.zip")


if __name__ == "__main__":
    unittest.main()

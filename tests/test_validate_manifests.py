import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_manifests import validate_manifest


class ValidateManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.app_dir = self.root / "my_app"
        (self.app_dir / "screenshots").mkdir(parents=True)
        (self.app_dir / "screenshots" / "main.webp").write_bytes(b"image")
        self.path = self.app_dir / "manifest.json"
        self.manifest = {
            "id": "my_app",
            "name": "My App",
            "version": "1.0.0",
            "authors": ["Developer"],
            "category": "Tools",
            "description": "A useful app.",
            "type": "app",
            "targets": ["esp32s3"],
            "license": "GPL-3.0",
            "source_repo": "https://github.com/developer/my-app",
            "source_branch": "main",
            "source_subdir": ".",
            "screenshots": [{"path": "screenshots/main.webp", "alt": "Main app screen"}],
            "reviewed": False,
        }

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_manifest(self):
        self.path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_valid_manifest(self):
        self.write_manifest()
        self.assertEqual(validate_manifest(self.path), [])

    def test_directory_must_match_id(self):
        self.manifest["id"] = "another_app"
        self.write_manifest()
        self.assertTrue(any("directory name" in error for error in validate_manifest(self.path)))

    def test_targets_must_be_supported_and_unique(self):
        self.manifest["targets"] = ["esp32s3", "esp32s3", "unsupported"]
        self.write_manifest()
        errors = validate_manifest(self.path)
        self.assertTrue(any("invalid target" in error for error in errors))
        self.assertTrue(any("duplicates" in error for error in errors))

    def test_source_subdir_cannot_escape_repository(self):
        self.manifest["source_subdir"] = "../private"
        self.write_manifest()
        self.assertTrue(any("source_subdir" in error for error in validate_manifest(self.path)))

    def test_screenshot_requires_existing_safe_path_and_alt_text(self):
        self.manifest["screenshots"] = [{"path": "screenshots/missing.webp", "alt": ""}]
        self.write_manifest()
        errors = validate_manifest(self.path)
        self.assertTrue(any("does not exist" in error for error in errors))
        self.assertTrue(any("alt must" in error for error in errors))

    def test_two_part_existing_release_versions_remain_valid(self):
        self.manifest["version"] = "1.2"
        self.write_manifest()
        self.assertFalse(any("version" in error for error in validate_manifest(self.path)))


if __name__ == "__main__":
    unittest.main()

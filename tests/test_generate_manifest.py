import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.generate_manifest import generate_manifest, write_manifest


class GenerateManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", "git@github.com:developer/my-app.git"],
            cwd=self.root,
            check=True,
        )
        runtime = {
            "id": "my_app",
            "name": "My App",
            "version": "1.0.0",
            "author": "Developer",
            "description": "A useful app.",
            "category": "Tools",
            "entry": "my_app.so",
            "target": "esp32s3",
            "api_version": 1,
        }
        (self.root / "manifest.json").write_text(json.dumps(runtime), encoding="utf-8")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_generates_values_from_runtime_and_git(self):
        manifest = generate_manifest(self.root, license_id="GPL-3.0")
        self.assertEqual(manifest["id"], "my_app")
        self.assertEqual(manifest["authors"], ["Developer"])
        self.assertEqual(manifest["targets"], ["esp32s3"])
        self.assertEqual(manifest["source_repo"], "https://github.com/developer/my-app")
        self.assertEqual(manifest["source_branch"], "main")
        self.assertEqual(manifest["source_subdir"], ".")
        self.assertFalse(manifest["reviewed"])

    def test_refuses_to_overwrite_output(self):
        output = self.root / "catalog.json"
        output.write_text("existing", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            write_manifest({"id": "my_app"}, output)

    def test_requires_license_when_runtime_omits_it(self):
        with self.assertRaisesRegex(ValueError, "license"):
            generate_manifest(self.root)


if __name__ == "__main__":
    unittest.main()

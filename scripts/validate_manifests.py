import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

REQUIRED_FIELDS = (
    "id",
    "name",
    "version",
    "authors",
    "category",
    "description",
    "type",
    "targets",
    "license",
    "source_repo",
    "source_branch",
    "source_subdir",
)
VALID_CATEGORIES = {
    "System",
    "Tools",
    "Games",
    "Bluetooth",
    "GPIO",
    "Infrared",
    "Media",
    "NFC",
    "RFID",
    "Sub-GHz",
    "USB",
}
VALID_TARGETS = {"esp32", "esp32s2", "esp32s3", "esp32c5", "esp32c6"}
ID_PATTERN = re.compile(r"[a-z][a-z0-9_]*")
VERSION_PATTERN = re.compile(r"\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z.-]+)?")
LICENSE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+-]*")
GITHUB_PATTERN = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+?(?:\.git)?")
SCREENSHOT_PATTERN = re.compile(r"screenshots/[A-Za-z0-9._/-]+\.(?:png|jpe?g|webp)", re.IGNORECASE)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _safe_relative_path(value, allow_dot=False):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    if allow_dot and value == ".":
        return True
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def validate_manifest(path):
    path = Path(path)
    errors = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        return [f"{path}: cannot read manifest: {error}"]
    except json.JSONDecodeError as error:
        return [f"{path}: invalid JSON: {error}"]

    if not isinstance(manifest, dict):
        return [f"{path}: manifest must be a JSON object"]

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"{path}: missing required field '{field}'")

    app_id = manifest.get("id")
    if not isinstance(app_id, str) or not ID_PATTERN.fullmatch(app_id):
        errors.append(f"{path}: 'id' must start with a lowercase letter and contain only lowercase letters, numbers, and underscores")
    elif path.parent.name != app_id:
        errors.append(f"{path}: directory name '{path.parent.name}' must match id '{app_id}'")

    for field in ("name", "description", "source_branch", "license"):
        if field in manifest and not _text(manifest[field]):
            errors.append(f"{path}: '{field}' must be non-empty text")

    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version):
        errors.append(f"{path}: 'version' must be a release version such as 1.0.0")

    if manifest.get("type") != "app":
        errors.append(f"{path}: 'type' must be 'app'")

    category = manifest.get("category")
    if category not in VALID_CATEGORIES:
        errors.append(f"{path}: invalid category '{category}'")

    authors = manifest.get("authors")
    if not isinstance(authors, list) or not authors or any(not _text(author) for author in authors):
        errors.append(f"{path}: 'authors' must be a non-empty array of names")

    targets = manifest.get("targets")
    if not isinstance(targets, list) or not targets:
        errors.append(f"{path}: 'targets' must be a non-empty array")
    else:
        invalid_targets = [target for target in targets if target not in VALID_TARGETS]
        for target in invalid_targets:
            errors.append(f"{path}: invalid target '{target}'")
        if len(targets) != len(set(targets)):
            errors.append(f"{path}: 'targets' must not contain duplicates")

    license_id = manifest.get("license")
    if isinstance(license_id, str) and license_id and not LICENSE_PATTERN.fullmatch(license_id):
        errors.append(f"{path}: 'license' must be an SPDX license identifier")

    source_repo = manifest.get("source_repo")
    if not isinstance(source_repo, str) or not GITHUB_PATTERN.fullmatch(source_repo):
        errors.append(f"{path}: 'source_repo' must be a public GitHub repository URL")

    source_subdir = manifest.get("source_subdir")
    if not _safe_relative_path(source_subdir, allow_dot=True):
        errors.append(f"{path}: 'source_subdir' must be '.' or a safe repository-relative path using forward slashes")

    if "reviewed" in manifest and not isinstance(manifest["reviewed"], bool):
        errors.append(f"{path}: 'reviewed' must be true or false")

    screenshots = manifest.get("screenshots", [])
    if not isinstance(screenshots, list):
        errors.append(f"{path}: 'screenshots' must be an array")
    elif len(screenshots) > 8:
        errors.append(f"{path}: no more than 8 screenshots are allowed")
    else:
        seen = set()
        app_dir = path.parent.resolve()
        for index, screenshot in enumerate(screenshots):
            label = f"{path}: screenshots[{index}]"
            if not isinstance(screenshot, dict):
                errors.append(f"{label} must be an object")
                continue
            image_path = screenshot.get("path")
            if not isinstance(image_path, str) or not SCREENSHOT_PATTERN.fullmatch(image_path) or not _safe_relative_path(image_path):
                errors.append(f"{label}.path must be a safe PNG, JPEG, or WebP path under screenshots/")
            else:
                normalized = image_path.lower()
                if normalized in seen:
                    errors.append(f"{label}.path is duplicated")
                seen.add(normalized)
                full_path = (path.parent / PurePosixPath(image_path)).resolve()
                try:
                    full_path.relative_to(app_dir)
                except ValueError:
                    errors.append(f"{label}.path escapes the app directory")
                else:
                    if not full_path.is_file():
                        errors.append(f"{label}.path does not exist under the app directory")
            if not _text(screenshot.get("alt")):
                errors.append(f"{label}.alt must be non-empty text")
            if "caption" in screenshot and not _text(screenshot["caption"]):
                errors.append(f"{label}.caption must be non-empty text when provided")

    return errors


def manifest_paths(root, requested):
    if requested:
        return [Path(item) for item in requested]
    return sorted(Path(root).glob("*/manifest.json"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate GhostESP catalog manifests")
    parser.add_argument("paths", nargs="*", help="Manifest paths; validates every app when omitted")
    parser.add_argument("--apps-dir", default="apps", help="Catalog apps directory")
    args = parser.parse_args(argv)

    paths = manifest_paths(args.apps_dir, args.paths)
    if not paths:
        print("No manifests found.", file=sys.stderr)
        return 1

    errors = [error for path in paths for error in validate_manifest(path)]
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(paths)} manifest(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

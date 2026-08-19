# Contributing to GhostESP App Catalog

New app developers should start with [Create and Submit a GhostESP App](docs/CREATE_AN_APP.md).

## How It Works

1. You develop and test the app in your own public source repository
2. You PR a catalog `manifest.json` pointing to that repository
3. Pull-request CI validates the submission and dry-runs every declared target build
4. Maintainers review and merge
5. Deployment CI rebuilds the app, uploads the `.gapp` to the R2 CDN, and regenerates the catalog

## Manifest Format

Generate a manifest from your source app:

```powershell
python scripts/generate_manifest.py C:\path\to\your_app --license GPL-3.0 --out apps/<your_app_id>/manifest.json
```

Alternatively, copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json`:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier (lowercase, underscores) |
| `name` | Yes | Display name |
| `version` | Yes | Release version (e.g., `1.0.0`) |
| `authors` | Yes | Array of author names |
| `category` | Yes | One of: System, Tools, Games, Bluetooth, GPIO, Infrared, Media, NFC, RFID, Sub-GHz, USB |
| `description` | Yes | Short description of what the app does |
| `type` | Yes | Must be `"app"` |
| `targets` | Yes | Array of targets: `esp32`, `esp32s2`, `esp32s3`, `esp32c5`, `esp32c6` |
| `license` | Yes | SPDX license identifier |
| `source_repo` | Yes | GitHub URL to your app source repo |
| `source_branch` | Yes | Branch to build from (e.g., `main`) |
| `source_subdir` | Yes | Subdirectory within the repo containing the app (e.g., `.` or `plugins/examples/my_app`) |
| `screenshots` | No | Ordered screenshot objects containing `path`, `alt`, and optional `caption` |
| `changelog` | No | Version changelog |

## Source Repo Requirements

Your source repo must:
1. Contain a valid `gbt` app project and runtime `manifest.json`
2. Build successfully with `gbt dist . --target esp32s3 --gapp`
3. Be a public GitHub repository that CI can clone without credentials
4. Use the same `id` and `version` in its runtime manifest as the catalog manifest

If your app is part of a larger repo, use `source_subdir` to point to the app directory. Pull-request CI clones the repository and builds every target listed in `targets`.

## Screenshots

Store up to eight marketplace screenshots under `apps/<your_app_id>/screenshots/` in this repository. PNG, JPEG, and WebP are supported. Paths are relative to the marketplace manifest, and every image requires useful alternative text:

```json
"screenshots": [
  {
    "path": "screenshots/main.webp",
    "alt": "Pong running in a portrait court with the player paddle at the bottom",
    "caption": "Portrait gameplay"
  }
]
```

The first screenshot is also emitted as the legacy `preview` catalog field. Published screenshot URLs are versioned with the app release.

## Example: Standalone app

```json
{
  "id": "my_app",
  "name": "My App",
  "version": "1.0.0",
  "authors": ["YourName"],
  "category": "Tools",
  "description": "A cool app.",
  "type": "app",
  "targets": ["esp32s3"],
  "license": "GPL-3.0",
  "source_repo": "https://github.com/YourName/my-ghostesp-app",
  "source_branch": "main",
  "source_subdir": ".",
  "changelog": "v1.0.0: Initial release",
  "reviewed": false
}
```

## Example: App in GhostESP firmware

```json
{
  "id": "my_app",
  "name": "My App",
  "version": "1.0.0",
  "authors": ["YourName"],
  "category": "Tools",
  "description": "A firmware-bundled app.",
  "type": "app",
  "targets": ["esp32s3"],
  "license": "GPL-3.0",
  "source_repo": "https://github.com/GhostESP-Revival/GhostESP",
  "source_branch": "Development-deki",
  "source_subdir": "plugins/examples/my_app",
  "changelog": "v1.0.0: Initial release",
  "reviewed": false
}
```

## Validate Locally

From the catalog repository root, run:

```powershell
python scripts/validate_manifests.py apps/<your_app_id>/manifest.json
```

Contributors leave `reviewed` set to `false`; maintainers control review status.

## Updating

Publish and test the source changes first. Increment the version in both runtime and catalog manifests, update `source_branch` if needed, update the changelog, and open a new PR.

## Rules

- Do not edit `catalog.json` directly - it is auto-generated
- Your source repo must be public
- The source and catalog `id` and `version` must match
- Respond to review feedback within 14 days

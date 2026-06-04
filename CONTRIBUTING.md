# Contributing to GhostESP App Catalog

## How It Works

1. You PR a `manifest.json` pointing to your source repo
2. Maintainers review and merge
3. CI clones your source, builds `.gapp` with `gbt`, uploads to R2 CDN

## Manifest Format

Copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json`:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier (lowercase, underscores) |
| `name` | Yes | Display name |
| `version` | Yes | Semantic version (e.g., `1.0.0`) |
| `authors` | Yes | Array of author names |
| `category` | Yes | One of: System, Tools, Games, Bluetooth, GPIO, Infrared, Media, NFC, RFID, Sub-GHz, USB |
| `description` | Yes | Short description of what the app does |
| `type` | Yes | Must be `"app"` |
| `targets` | Yes | Array of targets: `esp32`, `esp32s2`, `esp32s3`, `esp32c5`, `esp32c6` |
| `license` | Yes | SPDX license identifier |
| `source_repo` | Yes | GitHub URL to your app source repo |
| `source_branch` | Yes | Branch to build from (e.g., `main`) |
| `source_subdir` | Yes | Subdirectory within the repo containing the app (e.g., `.` or `plugins/examples/my_app`) |
| `preview` | No | Screenshot filename in the app directory (e.g., `screenshot.png`) |
| `changelog` | No | Version changelog |

## Source Repo Requirements

Your source repo must:
1. Contain a valid `gbt` app project
2. Build successfully with `gbt dist --target esp32s3 --gapp .`
3. Be a public GitHub repository

If your app is part of a larger repo, use `source_subdir` to point to the app directory.

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
  "source_branch": "two-point-zero",
  "source_subdir": "plugins/examples/my_app",
  "changelog": "v1.0.0: Initial release",
  "reviewed": false
}
```

## Updating

Increment the version in your manifest, update `source_branch`/`commit_sha` if needed, and open a new PR.

## Rules

- Do not edit `catalog.json` directly - it is auto-generated
- Your source repo must be public
- Respond to review feedback within 14 days

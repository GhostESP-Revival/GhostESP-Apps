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
| `source_repo` | No | GitHub URL to your app source repo (or leave empty if source is in this repo) |
| `commit_sha` | No | Commit hash with the source to build |
| `preview` | No | Screenshot filename in source directory (e.g., `screenshot.png`) |
| `changelog` | No | Version changelog |

## Source Repo Requirements

Your source repo must:
1. Contain a valid `gbt` app project
2. Build successfully with `gbt dist --target esp32s3 --gapp .`
3. Be a public GitHub repository

## Example

```
apps/my_app/
└── manifest.json    # Points to your external source repo
```

Your manifest.json:
```json
{
  "id": "my_app",
  "name": "My App",
  "version": "1.0.0",
  "authors": ["YourName"],
  "category": "Tools",
  "description": "A cool app for GhostESP.",
  "type": "app",
  "targets": ["esp32s3"],
  "license": "GPL-3.0",
  "source_repo": "https://github.com/YourName/my-ghostesp-app",
  "commit_sha": "abc123def456",
  "changelog": "v1.0.0: Initial release",
  "reviewed": false
}
```

## Updating

Increment the version in your manifest, update `commit_sha` to point to the new source commit, and open a new PR.

## Rules

- Do not edit `catalog.json` directly - it is auto-generated
- Your source repo must be public
- Respond to review feedback within 14 days

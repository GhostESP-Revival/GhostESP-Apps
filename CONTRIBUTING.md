# Contributing to GhostESP App Catalog

Thank you for your interest in contributing to the GhostESP marketplace!

## Requirements

1. **Open Source License** - Apps must be licensed under an open source license (GPL-3.0 recommended)
2. **No malicious code** - Apps must not cause harm to devices or data
3. **Working source code** - Your source must build successfully with `gbt`
4. **Unique ID** - Your app/asset ID must not conflict with existing entries

## Submitting an App

### Step 1: Prepare your source code

Your app source should be a valid `gbt` project that builds with:
```bash
gbt dist --target esp32s3 --gapp your_app/source/
```

### Step 2: Create your manifest

Copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json` and fill in all fields:

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
| `source_url` | No | Link to external source repo (if separate) |
| `changelog` | No | Version changelog |

### Step 3: Add your source code

Place your app source in `apps/<your_app_id>/source/`.

### Step 4: Open a Pull Request

1. Fork this repository
2. Create a branch: `git checkout -b yourname/your_app_id`
3. Commit your changes
4. Open a PR against `main`

CI will automatically validate your manifest. After review and merge, your app will be built and deployed to the CDN.

## Submitting an Asset Pack

Same process but:
1. Copy `templates/asset-manifest.json` to `assets/<your_pack_id>/manifest.json`
2. Place source files in `assets/<your_pack_id>/source/`
3. Build command: `gbt asset pack --archive your_pack/source/`

### Asset manifest fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `name` | Yes | Display name |
| `version` | Yes | Version string |
| `authors` | Yes | Array of author names |
| `category` | Yes | Category (e.g., Theme) |
| `type` | Yes | Must be `"asset"` |
| `description` | Yes | Short description |
| `contents` | No | Array of what's included (Icons, Background, Colors) |
| `license` | Yes | SPDX license identifier |

## Updating an App or Asset

Increment the version in your manifest and open a new PR. The CI will build and upload the new version.

## Rules

- Do not edit `catalog.json` directly - it is auto-generated
- Do not commit binary `.gapp` or `.gtheme` files - they are built by CI
- Keep source code clean and well-documented
- Respond to review feedback within 14 days or your submission may be removed

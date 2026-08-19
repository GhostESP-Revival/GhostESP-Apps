# GhostESP App Catalog

Community-driven catalog for GhostESP apps (`.gapp`).

## How It Works

1. **Contributors** PR a manifest pointing to their source repo
2. **Maintainers** review and merge
3. **CI** clones source, builds `.gapp` with `gbt`, uploads to Cloudflare R2
4. **Website** fetches `catalog.json` to display apps

## Submitting an App

Your public repository contains the app source and runtime manifest. This repository receives only a catalog manifest and optional marketplace screenshots.

Start with [Create and Submit a GhostESP App](docs/CREATE_AN_APP.md), then see [CONTRIBUTING.md](CONTRIBUTING.md) for the complete manifest reference.

Quick start:
1. Build and test the app from your own public GitHub repository
2. Fork this repository
3. Copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json`
4. Fill in `source_repo`, `source_branch`, and `source_subdir`
5. Run `python scripts/validate_manifests.py apps/<your_app_id>/manifest.json`
6. Optionally add screenshots under `apps/<your_app_id>/screenshots/`
7. Open a Pull Request

## Building from GhostESP firmware

Apps built from the GhostESP firmware tree use:
```json
{
  "source_repo": "https://github.com/GhostESP-Revival/GhostESP",
  "source_branch": "Development-deki",
  "source_subdir": "plugins/examples/your_app"
}
```

## CDN

Built `.gapp` files are hosted at `https://gesp.fuckyourcdn.com`.
Screenshots are hosted at `https://gesp.fuckyourcdn.com/apps/<id>/v<version>/screenshots/<filename>`.

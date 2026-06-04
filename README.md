# GhostESP App & Asset Catalog

Community-driven marketplace for GhostESP apps (`.gapp`) and asset packs (`.gtheme`).

## How It Works

1. **Contributors** submit apps and asset packs via Pull Request
2. **Maintainers** review and merge PRs
3. **CI automatically** builds binaries with `gbt` and uploads to Cloudflare R2 CDN
4. **The website** fetches `catalog.json` to display marketplace items

## Repository Structure

```
apps/                    # App manifests
  <app_id>/
    manifest.json        # App metadata + config
    source/              # App source code (built by gbt)
assets/                  # Asset pack manifests
  <asset_id>/
    manifest.json        # Asset metadata + config
    source/              # Asset source files (built by gbt)
templates/               # Manifest templates for contributors
catalog.json             # Auto-generated index (do not edit manually)
```

## Submitting an App

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

Quick start:
1. Fork this repo
2. Copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json`
3. Put your app source code in `apps/<your_app_id>/source/`
4. Open a Pull Request

## Submitting an Asset Pack

1. Fork this repo
2. Copy `templates/asset-manifest.json` to `assets/<your_pack_id>/manifest.json`
3. Put your asset source files in `assets/<your_pack_id>/source/`
4. Open a Pull Request

## CDN

All built binaries are hosted on Cloudflare R2 at `https://gesp.fuckyourcdn.com`.

## License

Individual apps and assets retain their own licenses as specified in their manifests.

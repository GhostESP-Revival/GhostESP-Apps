# GhostESP App Catalog

Community-driven catalog for GhostESP apps (`.gapp`).

## How It Works

1. **Contributors** PR a manifest pointing to their source repo
2. **Maintainers** review and merge
3. **CI** clones source, builds `.gapp` with `gbt`, uploads to Cloudflare R2
4. **Website** fetches `catalog.json` to display apps

## Submitting an App

See [CONTRIBUTING.md](CONTRIBUTING.md).

Quick start:
1. Fork this repo
2. Copy `templates/app-manifest.json` to `apps/<your_app_id>/manifest.json`
3. Fill in `source_repo` (your public GitHub repo) and `source_subdir`
4. Open a Pull Request

## Building from GhostESP firmware

Apps built from the GhostESP firmware tree use:
```json
{
  "source_repo": "https://github.com/GhostESP-Revival/GhostESP",
  "source_branch": "two-point-zero",
  "source_subdir": "plugins/examples/your_app"
}
```

## CDN

Built `.gapp` files are hosted at `https://gesp.fuckyourcdn.com`.

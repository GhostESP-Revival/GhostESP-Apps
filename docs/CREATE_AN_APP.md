# Create and Submit a GhostESP App

A GhostESP app uses two repositories:

- Your repository contains the app source, build files, SDK headers, and runtime `manifest.json`.
- This catalog repository contains only `apps/<app_id>/manifest.json` and optional marketplace screenshots.

Catalog CI clones your public source repository and builds the release. Do not commit generated `.gapp`, `.so`, `build/`, or `dist/` files to this catalog.

## 1. Install the build tool

Install Python, Git, and Ghost Build Tool:

```powershell
python -m pip install ghostbt==0.5.7
gbt setup --target esp32s3
```

Replace `esp32s3` with the target used by your device. ESP-IDF setup is required only once for each target. If a Windows build reports that `ESP_ROM_ELF_DIR` is undefined, activate ESP-IDF in that PowerShell session before building:

```powershell
. "$HOME\.ghostbt\esp-idf\export.ps1"
```

## 2. Create a standalone app repository

```powershell
gbt create my_app --name "My App"
cd my_app
git init
```

App IDs start with a lowercase letter and use only lowercase letters, numbers, and underscores.

The generated project contains:

```text
my_app/
  main/
    my_app.c
  sdk/
  CMakeLists.txt
  manifest.json
  sdkconfig.defaults
```

Edit `main/my_app.c` to implement the app. Edit the runtime `manifest.json` when the app needs permissions, hardware features, a new version, or different metadata.

## 3. Build and test

```powershell
gbt dist . --target esp32s3 --gapp
```

The release archive is written under `dist/`. Copy the generated `.gapp` to `ghostesp/apps/` on the SD card and reboot. Inside GhostESP, this directory is mounted as `/mnt/ghostesp/apps/`.

Test the generated package on compatible hardware before submitting it. Repeat the build for every target you intend to publish:

```powershell
gbt dist . --target esp32c5 --gapp
gbt dist . --target esp32s3 --gapp
```

## 4. Publish the source repository

Commit the source in your own repository and push it to a public GitHub repository. For example, with GitHub CLI:

```powershell
git add .
git commit -m "Initial release"
gh repo create my_app --public --source . --push
```

Catalog CI must be able to clone the repository and branch without credentials. The source repository must contain the runtime `manifest.json` in the directory identified by `source_subdir`.

## 5. Add the catalog manifest

Fork and clone this catalog repository. From its root, generate a catalog manifest from your source app:

```powershell
python scripts/generate_manifest.py C:\path\to\my_app --license GPL-3.0 --out apps/my_app/manifest.json
```

The generator reads shared metadata from the runtime manifest and reads the repository URL, branch, and source subdirectory from Git. It refuses to overwrite an existing file. You can instead copy `templates/app-manifest.json` to `apps/my_app/manifest.json` and fill it in manually.

Confirm these fields:

- `source_repo`: the public URL of your source repository.
- `source_branch`: the branch CI should build, usually `main`.
- `source_subdir`: `.` when the app is at the repository root, or its repository-relative directory.
- `targets`: every target that successfully produced and ran a `.gapp`.
- `license`: the SPDX identifier used by the source repository.

The catalog `id` and `version` must exactly match the runtime manifest in the source repository. Contributors leave `reviewed` set to `false`; maintainers control review status.

Validate the submission locally from the catalog root:

```powershell
python scripts/validate_manifests.py apps/my_app/manifest.json
```

## 6. Add optional screenshots

Store up to eight PNG, JPEG, or WebP images under:

```text
apps/my_app/screenshots/
```

Then add them to the catalog manifest:

```json
"screenshots": [
  {
    "path": "screenshots/main.webp",
    "alt": "My App showing its main status screen",
    "caption": "Main screen"
  }
]
```

Every screenshot needs useful alternative text. The first screenshot becomes the app preview.

## 7. Open the pull request

Commit only the catalog manifest and optional screenshots. Do not edit `catalog.json`; deployment regenerates it.

The pull-request checks:

1. Validate every catalog manifest and screenshot.
2. Clone your source repository at `source_branch`.
3. Confirm `source_subdir`, source `id`, and source `version`.
4. Build every declared target and verify the expected `.gapp` is produced.

After maintainers approve and merge the submission, deployment rebuilds the app, publishes it to the CDN, and regenerates `catalog.json`.

## Updating an app

Update and test the source repository first. Then change the catalog `version` and `changelog`, confirm the source runtime manifest has the same version, and open another catalog pull request.

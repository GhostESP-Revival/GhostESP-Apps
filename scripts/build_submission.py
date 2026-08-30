import argparse
import json
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path, PurePosixPath


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def target_manifest_name(catalog, target):
    mappings = catalog.get("target_manifests", {})
    name = mappings.get(target, "manifest.json") if isinstance(mappings, dict) else "manifest.json"
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"invalid target manifest path for {target}: {name!r}")
    return name


def build_submission(manifest_path, target, output_dir=None):
    manifest_path = Path(manifest_path).resolve()
    catalog = load_json(manifest_path)
    app_id = catalog["id"]
    version = catalog["version"]
    if target not in catalog["targets"]:
        raise ValueError(f"target '{target}' is not declared by {app_id}")

    with tempfile.TemporaryDirectory(prefix=f"ghostesp-{app_id}-") as temporary_directory:
        checkout = Path(temporary_directory) / "source"
        subprocess.run(
            [
                "git",
                "clone",
                "--depth=1",
                "--recurse-submodules",
                "--branch",
                catalog["source_branch"],
                catalog["source_repo"],
                str(checkout),
            ],
            check=True,
        )
        source_dir = checkout if catalog["source_subdir"] == "." else checkout / PurePosixPath(catalog["source_subdir"])
        if not source_dir.is_dir():
            raise FileNotFoundError(f"source_subdir does not exist: {catalog['source_subdir']}")

        selected_manifest_name = target_manifest_name(catalog, target)
        source_manifest_path = source_dir / PurePosixPath(selected_manifest_name)
        if not source_manifest_path.is_file():
            raise FileNotFoundError(f"source app has no {selected_manifest_name} in {catalog['source_subdir']}")
        source = load_json(source_manifest_path)
        for field in ("id", "version"):
            if source.get(field) != catalog[field]:
                raise ValueError(
                    f"source manifest {field} '{source.get(field)}' does not match catalog value '{catalog[field]}'"
                )

        destination = Path(output_dir).resolve() if output_dir else Path(temporary_directory) / "dist"
        destination.mkdir(parents=True, exist_ok=True)
        expected_name = f"{app_id}-{version}-{target}.gapp"
        if list(destination.rglob(expected_name)):
            raise FileExistsError(f"output already contains {expected_name}; choose an empty output directory")
        default_manifest_path = source_dir / "manifest.json"
        original_manifest = default_manifest_path.read_bytes() if default_manifest_path.is_file() else None
        if selected_manifest_name != "manifest.json":
            shutil.copyfile(source_manifest_path, default_manifest_path)
        try:
            subprocess.run(
                [
                    "gbt",
                    "dist",
                    str(source_dir),
                    "--target",
                    target,
                    "--gapp",
                    "--out",
                    str(destination),
                ],
                check=True,
            )
        finally:
            if selected_manifest_name != "manifest.json":
                if original_manifest is None:
                    default_manifest_path.unlink(missing_ok=True)
                else:
                    default_manifest_path.write_bytes(original_manifest)
        packages = list(destination.rglob(expected_name))
        if not packages:
            raise FileNotFoundError(f"build did not produce expected package: {expected_name}")
        print(packages[0])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Clone and dry-run a GhostESP catalog submission build")
    parser.add_argument("manifest", help="Catalog manifest to build")
    parser.add_argument("--target", required=True, help="Target declared by the catalog manifest")
    parser.add_argument("--out", help="Optional output directory")
    args = parser.parse_args(argv)
    try:
        build_submission(args.manifest, args.target, args.out)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"Submission build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

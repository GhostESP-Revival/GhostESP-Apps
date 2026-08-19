import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def git(app_path, *args):
    return subprocess.run(
        ["git", *args],
        cwd=app_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def github_url(value):
    value = value.strip()
    if value.endswith(".git"):
        value = value[:-4]
    match = re.fullmatch(r"git@github\.com:([^/]+/[^/]+)", value)
    if match:
        return f"https://github.com/{match.group(1)}"
    match = re.fullmatch(r"ssh://git@github\.com/([^/]+/[^/]+)", value)
    if match:
        return f"https://github.com/{match.group(1)}"
    if re.fullmatch(r"https://github\.com/[^/]+/[^/]+", value):
        return value
    raise ValueError("origin must be a public GitHub repository URL")


def generate_manifest(app_dir, license_id=None, author=None, targets=None, branch=None, repo=None, changelog=None):
    app_path = Path(app_dir).resolve()
    runtime_path = app_path / "manifest.json"
    if not runtime_path.is_file():
        raise FileNotFoundError(f"runtime manifest not found: {runtime_path}")
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    repo_root = Path(git(app_path, "rev-parse", "--show-toplevel"))
    source_subdir = app_path.relative_to(repo_root).as_posix() or "."
    source_repo = github_url(repo or git(app_path, "remote", "get-url", "origin"))
    source_branch = branch or git(app_path, "branch", "--show-current")
    if not source_branch:
        raise ValueError("cannot detect the source branch; pass --branch")

    authors = runtime.get("authors")
    if not isinstance(authors, list) or not authors:
        authors = [author or runtime.get("author")]
    if not authors or any(not isinstance(item, str) or not item.strip() for item in authors):
        raise ValueError("author is missing; pass --author")

    license_id = license_id or runtime.get("license")
    if not license_id:
        raise ValueError("license is missing; pass --license with an SPDX identifier")

    selected_targets = targets or runtime.get("targets") or [runtime.get("target", "esp32s3")]
    version = runtime.get("version", "0.1.0")
    return {
        "id": runtime["id"],
        "name": runtime.get("name", runtime["id"]),
        "version": version,
        "authors": authors,
        "category": runtime.get("category", "Tools"),
        "description": runtime.get("description", "A GhostESP native SD app."),
        "type": "app",
        "targets": selected_targets,
        "license": license_id,
        "source_repo": source_repo,
        "source_branch": source_branch,
        "source_subdir": source_subdir,
        "changelog": changelog or f"v{version}: Initial release",
        "reviewed": False,
    }


def write_manifest(manifest, output=None):
    text = json.dumps(manifest, indent=2) + "\n"
    if output is None:
        print(text, end="")
        return
    path = Path(output)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(path.resolve())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a catalog manifest from a GhostESP app repository")
    parser.add_argument("app_dir", help="Directory containing the app runtime manifest")
    parser.add_argument("--license", dest="license_id", help="SPDX license identifier")
    parser.add_argument("--author", help="Author when absent from the runtime manifest")
    parser.add_argument("--target", dest="targets", action="append", help="Release target; repeat for multiple targets")
    parser.add_argument("--branch", help="Source branch override")
    parser.add_argument("--repo", help="Public GitHub source repository override")
    parser.add_argument("--changelog", help="Initial catalog changelog")
    parser.add_argument("--out", help="Output path; prints JSON when omitted")
    args = parser.parse_args(argv)
    try:
        manifest = generate_manifest(
            args.app_dir,
            license_id=args.license_id,
            author=args.author,
            targets=args.targets,
            branch=args.branch,
            repo=args.repo,
            changelog=args.changelog,
        )
        write_manifest(manifest, args.out)
    except (FileNotFoundError, FileExistsError, KeyError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"Cannot generate catalog manifest: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

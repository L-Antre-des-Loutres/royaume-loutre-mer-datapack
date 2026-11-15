"""Assemble le datapack en jar Fabric sans code, à poser dans mods/.

Usage : python tools/build_jar.py   (écrit dans build/)
"""
import json
import sys
import zipfile
from pathlib import Path

ROOT_FILES = ("fabric.mod.json", "pack.mcmeta", "LICENSE")


def build_jar(repo_root: Path, out_dir: Path) -> Path:
    repo_root = Path(repo_root)
    out_dir = Path(out_dir)
    mod = json.loads((repo_root / "fabric.mod.json").read_text(encoding="utf-8"))
    jar = out_dir / f"{mod['id']}-{mod['version']}.jar"
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(jar, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ROOT_FILES:
            zf.write(repo_root / name, name)
        for path in sorted((repo_root / "data").rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(repo_root).as_posix())
    return jar


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    jar = build_jar(repo_root, repo_root / "build")
    print(jar)
    return 0


if __name__ == "__main__":
    sys.exit(main())

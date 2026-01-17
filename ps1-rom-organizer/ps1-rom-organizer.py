import re
import sys
from collections import defaultdict
from pathlib import Path


FLAGS = re.IGNORECASE | re.VERBOSE

DISC_RE = re.compile(
    r"""
    \s*
    \(?
    disc\s*\d+
    \)?
    \s*$
    """,
    FLAGS,
)


def remove_disc_suffix(name: str) -> str:
    """Remove a trailing disc indicator from a filename stem."""
    return DISC_RE.sub("", name).strip()


def referenced_files_from_cue(cue_path: Path) -> list[str]:
    """Return filenames referenced by FILE directives in a .cue file."""
    refs: list[str] = []

    with cue_path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if line.upper().startswith("FILE"):
                parts = line.split('"')
                if len(parts) >= 2:
                    refs.append(parts[1])

    return refs


def main() -> None:
    if len(sys.argv) < 2:
        script = Path(sys.argv[0]).name
        print(f"Usage: python {script} <roms_directory>")
        sys.exit(1)

    root = Path(sys.argv[1])

    if not root.is_dir():
        print(f"ERROR: not a directory: {root}")
        sys.exit(1)

    entry_exts = {".chd", ".cue", ".ccd", ".toc"}

    games: dict[str, list[Path]] = defaultdict(list)

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in entry_exts:
            continue

        base_title = remove_disc_suffix(path.stem)
        games[base_title].append(path)

    multi_root = root / "multi"
    multi_root.mkdir(exist_ok=True)

    # Move disc entry files into multi/<Game>/
    for game, files in games.items():
        game_dir = multi_root / game
        game_dir.mkdir(exist_ok=True)

        for src in files:
            dst = game_dir / src.name
            if src.resolve() != dst.resolve() and not dst.exists():
                src.rename(dst)

    # Move files referenced by .cue files
    for game, files in games.items():
        game_dir = multi_root / game

        for src in files:
            if src.suffix.lower() != ".cue":
                continue

            original_cue_dir = src.parent
            moved_cue_path = game_dir / src.name

            for ref_name in referenced_files_from_cue(moved_cue_path):
                ref_src = original_cue_dir / ref_name
                ref_dst = game_dir / ref_name

                if not ref_src.exists():
                    print(f"WARNING: missing referenced file: {ref_src}")
                    continue

                if ref_src.resolve() != ref_dst.resolve() and not ref_dst.exists():
                    ref_src.rename(ref_dst)

    # Write one .m3u file per game
    for game, files in games.items():
        m3u_path = root / f"{game}.m3u"

        with m3u_path.open("w", encoding="utf-8") as m3u:
            for src in sorted(files, key=lambda p: p.name):
                m3u.write(f"multi/{game}/{src.name}\n")


if __name__ == "__main__":
    main()

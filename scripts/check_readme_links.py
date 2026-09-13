#!/usr/bin/env python3
"""Fail if any SQLs/ problem file or folder isn't linked from README.md.

Run standalone, or wired up as the pre-commit hook installed by `make install-hooks`.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SQLS_DIR = PROJECT_ROOT / "SQLs"
README = PROJECT_ROOT / "README.md"


def expected_paths() -> list[str]:
    paths = []

    for child in sorted(SQLS_DIR.iterdir()):
        if child.name in ("leetcode", "other_problems"):
            continue
        if child.is_file() and child.suffix in (".md", ".sql"):
            paths.append(f"SQLs/{child.name}")

    for subdir in ("leetcode", "other_problems"):
        base = SQLS_DIR / subdir
        if not base.is_dir():
            continue
        for folder in sorted(base.iterdir()):
            if folder.is_dir():
                paths.append(f"SQLs/{subdir}/{folder.name}/description.md")

    return paths


def main() -> int:
    readme_text = README.read_text()
    missing = [p for p in expected_paths() if p not in readme_text]

    if missing:
        print("README.md is missing a link for the following problem(s):")
        for path in missing:
            print(f"  - {path}")
        print("\nAdd a row for each to the appropriate table in the SQLs section of README.md.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

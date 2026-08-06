#!/usr/bin/env python3
"""Execute the Setup SQL block from a problem's setup.md against the local MySQL instance."""

import re
import sys
from pathlib import Path

import mysql.connector

PROJECT_ROOT = Path(__file__).parent.parent

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "my-secret-pw",
}


def find_setup_file(target: str) -> Path:
    """Resolve a general .md filename/path, or a problem folder name, to its setup source."""
    # Absolute or relative path (e.g. "SQLs/window_frame.md", "SQLs/leetcode/<folder>"): resolve directly.
    if "/" in target or Path(target).is_absolute():
        path = Path(target)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if path.is_dir():
            path = path / "setup.md"
        if not path.exists():
            sys.exit(f"Error: file not found: '{path}'")
        return path

    # Bare "<name>.md": a general single-file problem — search all subdirectories by filename.
    if target.endswith(".md"):
        matches = list(PROJECT_ROOT.rglob(target))
        if not matches:
            sys.exit(f"Error: '{target}' not found under {PROJECT_ROOT}")
        if len(matches) > 1:
            paths = "\n  ".join(str(p) for p in matches)
            sys.exit(f"Error: multiple files named '{target}' found:\n  {paths}\nProvide a more specific path.")
        return matches[0]

    # Bare name with no extension: a problem folder name (e.g. under SQLs/leetcode/ or SQLs/other_problems/).
    matches = [p / "setup.md" for p in PROJECT_ROOT.rglob(target) if p.is_dir() and (p / "setup.md").exists()]
    if not matches:
        sys.exit(f"Error: no problem folder named '{target}' with a setup.md found under {PROJECT_ROOT}")
    if len(matches) > 1:
        paths = "\n  ".join(str(p) for p in matches)
        sys.exit(f"Error: multiple problem folders named '{target}' found:\n  {paths}\nProvide a more specific path.")
    return matches[0]


def extract_setup_sql(md_path: Path, setup_num: int = 1) -> str:
    text = md_path.read_text()
    # Setup 1 lives under "## Setup"; Setup N (N>=2) under "## SetupN".
    heading = "Setup" if setup_num == 1 else f"Setup{setup_num}"
    setup_match = re.search(rf"^##\s+{heading}\s*$", text, re.MULTILINE)
    if not setup_match:
        sys.exit(f"Error: no '## {heading}' section found in '{md_path}'")

    # Extract the first ```sql ... ``` block after the Setup heading
    after_setup = text[setup_match.end():]
    sql_match = re.search(r"```sql\s*\n(.*?)```", after_setup, re.DOTALL)
    if not sql_match:
        sys.exit(f"Error: no SQL code block found under '## {heading}' in '{md_path}'")

    return sql_match.group(1).strip()


def execute_sql(sql: str) -> None:
    # Split on semicolons, skip empty statements
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        for stmt in statements:
            print(f"  > {stmt[:80]}{'...' if len(stmt) > 80 else ''}")
            cursor.execute(stmt)
        conn.commit()
        print(f"\nDone — {len(statements)} statement(s) executed successfully.")
    finally:
        cursor.close()
        conn.close()


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: setup_sql.py <problem-folder> [setup_num]")

    target = sys.argv[1]
    setup_num = 1
    if len(sys.argv) >= 3:
        try:
            setup_num = int(sys.argv[2])
        except ValueError:
            sys.exit(f"Error: setup number must be an integer, got '{sys.argv[2]}'")

    md_path = find_setup_file(target)

    print(f"File   : {md_path.relative_to(PROJECT_ROOT)}")
    print(f"Setup  : {'Setup' if setup_num == 1 else f'Setup{setup_num}'}")

    sql = extract_setup_sql(md_path, setup_num)
    print(f"Host   : {DB_CONFIG['host']}:{DB_CONFIG['port']}\n")

    execute_sql(sql)


if __name__ == "__main__":
    main()

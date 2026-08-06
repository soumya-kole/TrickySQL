# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of advanced SQL problems (interview prep and LeetCode) solved in MySQL. General interview-prep problems (`SQLs/*.md`) each live in a single `.md` file combining problem description, sample data setup, and one or more query solutions. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` instead live one-per-folder, split into three files — see [.md file structure](#md-file-structure) below.

## Database environment

Two independent MySQL instances, each started with `docker-compose up -d` from their respective directory:

| Directory | Purpose | Credentials |
|-----------|---------|-------------|
| `/` (root) | General / LeetCode problems | admin/admin (GUI), root/my-secret-pw (scripts) |
| `Meta/` | Meta Data Engineering interview problems | admin/admin |

Both expose MySQL on port 3306. Start/stop from the relevant directory:

```bash
docker-compose up -d
docker-compose down
```

## Loading problem data

```bash
# General SQLs/*.md problems — by filename (searches all subdirectories automatically)
make setup The_Number_of_Passengers_in_Each_Bus_1.md

# By relative path
make setup SQLs/window_frame.md

# SQLs/leetcode/ and SQLs/other_problems/ problems — by problem folder name
make setup 2142-the-number-of-passengers-in-each-bus-i
make setup exchange-seats-within-department
```

This runs `scripts/setup_sql.py` via `uv`. For a `.md` target it extracts the `## Setup` SQL block from that file; for a folder-name target (`SQLs/leetcode/`, `SQLs/other_problems/`) it reads `setup.md` inside that folder instead. Either way, the SQL runs against `127.0.0.1:3306` as root.

A setup source may define multiple setups (`## Setup`, `## Setup2`, `## Setup3`, …) holding alternative datasets. `make setup` loads `## Setup` by default; pass a number as the second argument to load another:

```bash
make setup The_Number_of_Passengers_in_Each_Bus_2.md      # uses ## Setup
make setup 2153-the-number-of-passengers-in-each-bus-ii 2 # uses ## Setup2
```

Python dependencies are managed with `uv`. After cloning, run `uv sync` once to create `.venv`.

## .md file structure

**General problems** (`SQLs/*.md`, `Meta/`) use a single structured file consumed by `make setup`:

```
## Description   ← problem statement
## Setup         ← DDL + INSERT statements in a ```sql block (required for make setup)
## Solutions     ← one or more named solutions in ```sql blocks
```

A file may also include optional `## Setup2`, `## Setup3`, … sections, each a self-contained `sql` block holding an alternative dataset (e.g. an edge case the default data does not exercise).

**`SQLs/leetcode/` and `SQLs/other_problems/` problems** instead live one-per-folder, each containing three files:

- `description.md` — the title heading and `## Description` (problem statement + examples)
- `setup.md` — `## Setup` (and optional `## Setup2`, `## Setup3`, …), each a self-contained `sql` block followed by a `make setup <folder-name> [N]` snippet
- `solutions.md` — one or more `## Solution N[: name]` sections with explanation and `sql` code block(s)

`SQLs/leetcode/` folders are named `<zero-padded LeetCode number>-<kebab-case-title>` (e.g. `2142-the-number-of-passengers-in-each-bus-i`) and the `description.md` heading is `# [NUM. Title](url)`. `SQLs/other_problems/` folders (non-LeetCode or modified problems) are named `<kebab-case-title>` (e.g. `exchange-seats-within-department`), no number prefix.

## Adding a new problem

**General problem:**

1. Create `SQLs/<Problem_Name>.md` following the general structured format above.
2. The `## Setup` block must be self-contained: `CREATE DATABASE IF NOT EXISTS demo; USE demo;` then `DROP`/`CREATE`/`INSERT` in dependency order so it is safe to re-run.
3. (Optional) Add `## Setup2`, `## Setup3`, … sections for alternative datasets, following the same self-contained pattern.
4. `make setup <filename.md>` must run cleanly before committing.

**LeetCode problem:**

1. Create `SQLs/leetcode/<num>-<kebab-case-title>/` with `description.md`, `setup.md`, `solutions.md` following the structure above.
2. `setup.md`'s `## Setup` block must be self-contained, same rule as above; add `## Setup2`, … there for alternative datasets.
3. `make setup <num>-<kebab-case-title>` must run cleanly before committing.

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. `make setup <kebab-case-title>` must run cleanly before committing.

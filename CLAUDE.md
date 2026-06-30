# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of advanced SQL problems (interview prep and LeetCode) solved in MySQL. Each problem lives in a `.md` file that combines problem description, sample data setup, and one or more query solutions.

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
# By filename (searches all subdirectories automatically)
make setup The_Number_of_Passengers_in_Each_Bus_1.md

# By relative path
make setup SQLs/leetcode/The_Number_of_Passengers_in_Each_Bus_2.md
```

This runs `scripts/setup_sql.py` via `uv`, which extracts the `## Setup` SQL block from the file and executes it against `127.0.0.1:3306` as root.

A file may define multiple setups (`## Setup`, `## Setup2`, `## Setup3`, …) holding alternative datasets. `make setup` loads `## Setup` by default; pass a number as the second argument to load another:

```bash
make setup The_Number_of_Passengers_in_Each_Bus_2.md      # uses ## Setup
make setup The_Number_of_Passengers_in_Each_Bus_2.md 2    # uses ## Setup2
```

Python dependencies are managed with `uv`. After cloning, run `uv sync` once to create `.venv`.

## .md file structure

Each problem file uses the structured format consumed by `make setup`:

```
## Description   ← problem statement
## Setup         ← DDL + INSERT statements in a ```sql block (required for make setup)
## Solutions     ← one or more named solutions in ```sql blocks
```

A file may also include optional `## Setup2`, `## Setup3`, … sections, each a self-contained `sql` block holding an alternative dataset (e.g. an edge case the default data does not exercise).

## Adding a new problem

1. Create `SQLs/leetcode/<Problem_Name>.md` following the structured format above.
2. The `## Setup` block must be self-contained: `CREATE DATABASE IF NOT EXISTS demo; USE demo;` then `DROP`/`CREATE`/`INSERT` in dependency order so it is safe to re-run.
3. (Optional) Add `## Setup2`, `## Setup3`, … sections for alternative datasets, following the same self-contained pattern.
4. `make setup <filename.md>` must run cleanly before committing.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of advanced SQL problems (interview prep and LeetCode) solved in MySQL. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` live one-per-folder, split into three files — see [.md file structure](#md-file-structure) below. `Meta/` (a separate corpus of Meta Data Engineering interview problems) instead uses a single combined `.md` file per problem.

## Database environment

Two independent MySQL instances, each started with `docker-compose up -d` from their respective directory:

| Directory | Purpose | Credentials |
|-----------|---------|-------------|
| `/` (root) | LeetCode / other problems | admin/admin (GUI), root/my-secret-pw (scripts) |
| `Meta/` | Meta Data Engineering interview problems | admin/admin |

Both expose MySQL on port 3306. Start/stop from the relevant directory:

```bash
docker-compose up -d
docker-compose down
```

## Loading problem data

```bash
# SQLs/leetcode/ and SQLs/other_problems/ problems — by problem folder name
make setup 2142-the-number-of-passengers-in-each-bus-i
make setup exchange-seats-within-department

# A single-file general problem (e.g. under Meta/) — by filename (searches all
# subdirectories automatically) or by relative path
make setup My_Problem.md
make setup Meta/My_Problem.md
```

This runs `scripts/setup_sql.py` via `uv`. For a `.md` target it extracts the `## Setup` SQL block from that file; for a folder-name target (`SQLs/leetcode/`, `SQLs/other_problems/`) it reads `setup.md` inside that folder instead. Either way, the SQL runs against `127.0.0.1:3306` as root.

A setup source may define multiple setups (`## Setup`, `## Setup2`, `## Setup3`, …) holding alternative datasets. `make setup` loads `## Setup` by default; pass a number as the second argument to load another:

```bash
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

**LeetCode problem:**

1. Create `SQLs/leetcode/<num>-<kebab-case-title>/` with `description.md`, `setup.md`, `solutions.md` following the structure above.
2. `setup.md`'s `## Setup` block must be self-contained, same rule as above; add `## Setup2`, … there for alternative datasets.
3. `make setup <num>-<kebab-case-title>` must run cleanly before committing.
4. Add a row for it to the **LeetCode problems** table in the [SQLs section of README.md](README.md#sqls), keeping the table sorted by problem number — see [Updating README.md](#updating-readmemd) below.

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. `make setup <kebab-case-title>` must run cleanly before committing.
3. Add a row for it to the **Other problems** table in the [SQLs section of README.md](README.md#sqls) — see [Updating README.md](#updating-readmemd) below.

## Updating README.md

Every folder added under `SQLs/` must get a row in the matching table (LeetCode / Other problems) in README.md's `## SQLs` section, with three columns:

- **SQL Link** — link to `description.md` inside the `leetcode`/`other_problems` folder.
- **Level** — Easy/Medium/Hard. For LeetCode problems, use the problem's actual LeetCode difficulty (don't guess — many locked/older problems are rated differently than intuition suggests; verify via web search if unsure). For non-LeetCode problems, use your own judgment of query complexity.
- **Tags** — one or more short tags describing the SQL techniques used (e.g. `Recursive CTE`, `Window Functions`, `Pivot Table`, `Date Manipulation`, `Gaps & Islands`, `Self Join`), derived from what the solution(s) actually do.

A git pre-commit hook (`scripts/check_readme_links.py`, installed via `make install-hooks`) blocks commits that add a `SQLs/` problem without a corresponding link in README.md — but it only checks that a link exists, not that Level/Tags are filled in correctly, so still add the full row rather than relying on the hook to catch a missing link after the fact.

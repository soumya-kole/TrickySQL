# TRICKY SQL

This repository contains tricky and advanced SQL problems frequently asked in job interviews, solved in MySQL. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` live one-per-folder, split across `description.md`, `setup.md`, and `solutions.md` — see [Problem file structure](#problem-file-structure).

## Prerequisite

- Docker should be running on your system.
- [uv](https://github.com/astral-sh/uv) for running the Python helper scripts. After cloning, run `uv sync` once to create the `.venv`.
- Run `make install-hooks` once after cloning to enable a pre-commit hook that blocks commits which add a problem under `SQLs/` without a corresponding link in [PROBLEMS.md](PROBLEMS.md).

## Environment

Clone the repository and go to the root folder of the cloned repo. Start the database with:

```bash
docker compose up -d
```

Shut it down from the same directory with:

```bash
docker compose down
```

This exposes MySQL on port `3306`.

## Connect Database

You can use any GUI tool like DBeaver, connecting with user/password `admin/admin`. To change the credentials, edit `docker-compose.yaml`. (The helper scripts connect as `root` / `my-secret-pw`.)

## Problem file structure

Problems under `SQLs/leetcode/` and `SQLs/other_problems/` live one-per-folder, each containing:

- `description.md` — the problem statement and examples
- `setup.md` — the `## Setup` (and optional `## Setup2`, …) `sql` block(s)
- `solutions.md` — one or more named solutions, each in its own `sql` block

`SQLs/leetcode/` folders are named `<zero-padded LeetCode number>-<kebab-case-title>` (e.g. `2142-the-number-of-passengers-in-each-bus-i`); `SQLs/other_problems/` folders (non-LeetCode or modified problems) are named `<kebab-case-title>` (e.g. `exchange-seats-within-department`).

A general problem can instead live as a single `.md` file anywhere under `SQLs/` (`## Description`, `## Setup`, `## Solutions`, and optional `## Setup2`, `## Setup3`, … sections for alternative datasets).

## Loading problem data

Use `make setup` to load a problem's data into the running MySQL instance.

```bash
# SQLs/leetcode/ and SQLs/other_problems/ problems — by problem folder name
make setup 2142-the-number-of-passengers-in-each-bus-i
make setup exchange-seats-within-department

# A single-file general problem — by filename (searches all
# subdirectories automatically) or by relative path
make setup My_Problem.md
make setup SQLs/My_Problem.md
```

To load an alternative setup, pass its number as a second argument. With no number the default `## Setup` is used:

```bash
make setup 2153-the-number-of-passengers-in-each-bus-ii 2     # uses ## Setup2
```

## How to add a new problem

**LeetCode problem:**

1. Create `SQLs/leetcode/<num>-<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md` following the structure above.
2. `setup.md`'s `## Setup` block follows the same self-contained rule as above; add `## Setup2`, … there for alternative datasets.
3. Verify the data loads cleanly before committing:

   ```bash
   make setup <num>-<kebab-case-title>
   ```

4. Add a row for it to the **LeetCode problems** table in [PROBLEMS.md](PROBLEMS.md), keeping the table sorted by problem number.

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. Verify the data loads cleanly before committing:

   ```bash
   make setup <kebab-case-title>
   ```

3. Add a row for it to the **Other problems** table in [PROBLEMS.md](PROBLEMS.md).

Each table row needs a **SQL Link** (`description.md` inside the problem folder), a **Level** (for LeetCode problems, use the problem's real LeetCode difficulty rather than guessing), and one or more **Tags** describing the SQL techniques the solution uses (e.g. `Recursive CTE`, `Window Functions`, `Pivot Table`).

A pre-commit hook (enabled via `make install-hooks`, see [Prerequisite](#prerequisite)) blocks commits that add a problem under `SQLs/` without a matching link in [PROBLEMS.md](PROBLEMS.md) — but it only checks that a link exists, not that Level/Tags are correct, so don't rely on it in place of adding the full row.

## SQLs

The full problem list, with difficulty and technique tags, lives in [PROBLEMS.md](PROBLEMS.md).

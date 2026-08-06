# TRICKY SQL

This repository contains tricky and advanced SQL problems frequently asked in job interviews, solved in MySQL. General problems each live in a single `.md` file that bundles the problem description, the data setup, and one or more query solutions. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` instead live one-per-folder, split across `description.md`, `setup.md`, and `solutions.md` — see [Problem file structure](#problem-file-structure).

## Prerequisite

- Docker should be running on your system.
- [uv](https://github.com/astral-sh/uv) for running the Python helper scripts. After cloning, run `uv sync` once to create the `.venv`.

## Environment

Clone the repository and go to the root folder of the cloned repo. Start the database with:

```bash
docker-compose up -d
```

Shut it down from the same directory with:

```bash
docker-compose down
```

This exposes MySQL on port `3306`. There is a second, independent MySQL instance under `Meta/` for the Meta Data Engineering problems — start/stop it the same way from inside that directory.

## Connect Database

You can use any GUI tool like DBeaver, connecting with user/password `admin/admin`. To change the credentials, edit `docker-compose.yaml`. (The helper scripts connect as `root` / `my-secret-pw`.)

## Problem file structure

General problems (`SQLs/*.md`) follow this layout:

```
## Description   ← the problem statement
## Setup         ← DDL + INSERT statements in a ```sql block
## Solutions     ← one or more named solutions in ```sql blocks
```

A file may also define additional setups (`## Setup2`, `## Setup3`, …) holding alternative datasets — for example, an edge-case dataset that exercises a tricky path the default data does not.

Problems under `SQLs/leetcode/` and `SQLs/other_problems/` instead live one-per-folder, each containing:

- `description.md` — the problem statement and examples
- `setup.md` — the `## Setup` (and optional `## Setup2`, …) `sql` block(s)
- `solutions.md` — one or more named solutions, each in its own `sql` block

`SQLs/leetcode/` folders are named `<zero-padded LeetCode number>-<kebab-case-title>` (e.g. `2142-the-number-of-passengers-in-each-bus-i`); `SQLs/other_problems/` folders (non-LeetCode or modified problems) are named `<kebab-case-title>` (e.g. `exchange-seats-within-department`).

## Loading problem data

Use `make setup` to load a problem's data into the running MySQL instance.

```bash
# General SQLs/*.md problems — by filename (all subdirectories are searched automatically)
make setup The_Number_of_Passengers_in_Each_Bus_1.md

# By relative path
make setup SQLs/window_frame.md

# SQLs/leetcode/ and SQLs/other_problems/ problems — by problem folder name
make setup 2142-the-number-of-passengers-in-each-bus-i
make setup exchange-seats-within-department
```

To load an alternative setup, pass its number as a second argument. With no number the default `## Setup` is used:

```bash
make setup The_Number_of_Passengers_in_Each_Bus_2.md          # uses ## Setup
make setup 2153-the-number-of-passengers-in-each-bus-ii 2     # uses ## Setup2
```

## How to add a new problem

**General problem:**

1. Create `SQLs/<Problem_Name>.md`.
2. Add the three sections in order:
   - `## Description` — the problem statement.
   - `## Setup` — a self-contained `sql` block. Begin with `CREATE DATABASE IF NOT EXISTS demo; USE demo;`, then `DROP` / `CREATE` / `INSERT` the tables in dependency order so the block is safe to re-run.
   - `## Solutions` — one or more solutions, each in its own `sql` block.
3. (Optional) Add a `## Setup2`, `## Setup3`, … section for any alternative dataset, following the same self-contained pattern as `## Setup`.
4. Verify the data loads cleanly before committing:

   ```bash
   make setup <Problem_Name>.md
   ```

**LeetCode problem:**

1. Create `SQLs/leetcode/<num>-<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md` following the structure above.
2. `setup.md`'s `## Setup` block follows the same self-contained rule as above; add `## Setup2`, … there for alternative datasets.
3. Verify the data loads cleanly before committing:

   ```bash
   make setup <num>-<kebab-case-title>
   ```

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. Verify the data loads cleanly before committing:

   ```bash
   make setup <kebab-case-title>
   ```

## SQLs

1. [explode implementation](SQLs/explode_demo.sql)
2. [windowing](SQLs/window_frame.md)
3. [exchange seat](SQLs/other_problems/exchange-seats-within-department/description.md)
4. [Customer with increasing purchase](SQLs/CustomerWithIncreasingPurchase.md)
5. [Hierarchical query in mysql](SQLs/connect_by_implementation_mysql.md)
6. [The Number of Passengers in Each Bus I](SQLs/leetcode/2142-the-number-of-passengers-in-each-bus-i/description.md)
7. [The Number of Passengers in Each Bus II](SQLs/leetcode/2153-the-number-of-passengers-in-each-bus-ii/description.md)
8. [Find Median Given Frequency of Numbers](SQLs/leetcode/0571-find-median-given-frequency-of-numbers/description.md)
9. [Consecutive Available Seats](SQLs/leetcode/0603-consecutive-available-seats/description.md)
10. [Generate the Invoice](SQLs/leetcode/2362-generate-the-invoice/description.md)

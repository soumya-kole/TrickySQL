# TRICKY SQL

This repository contains tricky and advanced SQL problems frequently asked in job interviews, solved in MySQL. Each problem lives in a single `.md` file that bundles the problem description, the data setup, and one or more query solutions.

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

Every problem file follows the same layout:

```
## Description   ← the problem statement
## Setup         ← DDL + INSERT statements in a ```sql block
## Solutions     ← one or more named solutions in ```sql blocks
```

A file may also define additional setups (`## Setup2`, `## Setup3`, …) holding alternative datasets — for example, an edge-case dataset that exercises a tricky path the default data does not.

## Loading problem data

Use `make setup` to load a problem's data into the running MySQL instance. It extracts the `## Setup` SQL block from the file and executes it.

```bash
# By filename (all subdirectories are searched automatically)
make setup The_Number_of_Passengers_in_Each_Bus_1.md

# By relative path
make setup SQLs/leetcode/The_Number_of_Passengers_in_Each_Bus_2.md
```

To load an alternative setup, pass its number as a second argument. With no number the default `## Setup` is used:

```bash
make setup The_Number_of_Passengers_in_Each_Bus_2.md      # uses ## Setup
make setup The_Number_of_Passengers_in_Each_Bus_2.md 2    # uses ## Setup2
```

## How to add a new problem

1. Create `SQLs/leetcode/<Problem_Name>.md`.
2. Add the three sections in order:
   - `## Description` — the problem statement.
   - `## Setup` — a self-contained `sql` block. Begin with `CREATE DATABASE IF NOT EXISTS demo; USE demo;`, then `DROP` / `CREATE` / `INSERT` the tables in dependency order so the block is safe to re-run.
   - `## Solutions` — one or more solutions, each in its own `sql` block.
3. (Optional) Add a `## Setup2`, `## Setup3`, … section for any alternative dataset, following the same self-contained pattern as `## Setup`.
4. Verify the data loads cleanly before committing:

   ```bash
   make setup <Problem_Name>.md
   ```

## SQLs

1. [explode implementation](SQLs/explode_demo.sql)
2. [windowing](SQLs/window_frame.md)
3. [exchange seat](SQLs/exchange_seat.md)
4. [Customer with increasing purchase](SQLs/CustomerWithIncreasingPurchase.md)
5. [Hierarchical query in mysql](SQLs/connect_by_implementation_mysql.md)
6. [The Number of Passengers in Each Bus I](SQLs/leetcode/The_Number_of_Passengers_in_Each_Bus_1.md)
7. [The Number of Passengers in Each Bus II](SQLs/leetcode/The_Number_of_Passengers_in_Each_Bus_2.md)

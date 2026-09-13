# TRICKY SQL

This repository contains tricky and advanced SQL problems frequently asked in job interviews, solved in MySQL. General problems each live in a single `.md` file that bundles the problem description, the data setup, and one or more query solutions. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` instead live one-per-folder, split across `description.md`, `setup.md`, and `solutions.md` — see [Problem file structure](#problem-file-structure).

## Prerequisite

- Docker should be running on your system.
- [uv](https://github.com/astral-sh/uv) for running the Python helper scripts. After cloning, run `uv sync` once to create the `.venv`.
- Run `make install-hooks` once after cloning to enable a pre-commit hook that blocks commits which add a problem under `SQLs/` without a corresponding link in this README.

## Environment

Clone the repository and go to the root folder of the cloned repo. Start the database with:

```bash
docker compose up -d
```

Shut it down from the same directory with:

```bash
docker compose down
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

5. Add a row for it to the **General problems** table in the [SQLs](#sqls) section below.

**LeetCode problem:**

1. Create `SQLs/leetcode/<num>-<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md` following the structure above.
2. `setup.md`'s `## Setup` block follows the same self-contained rule as above; add `## Setup2`, … there for alternative datasets.
3. Verify the data loads cleanly before committing:

   ```bash
   make setup <num>-<kebab-case-title>
   ```

4. Add a row for it to the **LeetCode problems** table in the [SQLs](#sqls) section below, keeping the table sorted by problem number.

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. Verify the data loads cleanly before committing:

   ```bash
   make setup <kebab-case-title>
   ```

3. Add a row for it to the **Other problems** table in the [SQLs](#sqls) section below.

Each table row needs a **SQL Link** (the file itself for a general problem, or `description.md` for a folder-based one), a **Level** (for LeetCode problems, use the problem's real LeetCode difficulty rather than guessing), and one or more **Tags** describing the SQL techniques the solution uses (e.g. `Recursive CTE`, `Window Functions`, `Pivot Table`).

A pre-commit hook (enabled via `make install-hooks`, see [Prerequisite](#prerequisite)) blocks commits that add a problem under `SQLs/` without a matching link somewhere in this README — but it only checks that a link exists, not that Level/Tags are correct, so don't rely on it in place of adding the full row.

## SQLs

### General problems

| SQL Link | Level | Tags |
|---|---|---|
| [Explode Implementation](SQLs/explode_demo.sql) | Medium | Recursive CTE, String Manipulation |
| [Moving Average with Window Frames](SQLs/window_frame.md) | Easy | Window Functions, Moving Average |
| [Hierarchical Query in MySQL (CONNECT BY equivalent)](SQLs/connect_by_implementation_mysql.md) | Medium | Recursive CTE, Hierarchical Query |
| [Customers With Strictly Increasing Purchases](SQLs/CustomerWithIncreasingPurchase.md) | Hard | Window Functions, Date Manipulation, Gaps & Islands |
| [Paired Products (Frequently Bought Together)](SQLs/PairedProducts.md) | Medium | Self Join, Aggregation, Top-N |
| [Split Full Name into First/Middle/Last](SQLs/first_middle_last_name.sql) | Easy | String Manipulation |
| [Match Win/Loss Summary](SQLs/match_win_summary.sql) | Easy | Union, Aggregation, CASE Expressions |
| [Start and End Location of a Trip](SQLs/start_end_location.sql) | Medium | Full Outer Join, Graph Traversal |

### LeetCode problems

| SQL Link | Level | Tags |
|---|---|---|
| [180. Consecutive Numbers](SQLs/leetcode/0180-consecutive-numbers/description.md) | Medium | Window Functions, Gaps & Islands |
| [197. Rising Temperature](SQLs/leetcode/0197-rising-temperature/description.md) | Easy | Self Join, Window Functions, Date Manipulation |
| [571. Find Median Given Frequency of Numbers](SQLs/leetcode/0571-find-median-given-frequency-of-numbers/description.md) | Hard | Recursive CTE, Window Functions, Median |
| [579. Find Cumulative Salary of an Employee](SQLs/leetcode/0579-find-cumulative-salary-of-an-employee/description.md) | Hard | Window Functions, Ranking, Running Total |
| [603. Consecutive Available Seats](SQLs/leetcode/0603-consecutive-available-seats/description.md) | Easy | Self Join, Window Functions, Gaps & Islands |
| [612. Shortest Distance in a Plane](SQLs/leetcode/0612-shortest-distance-in-a-plane/description.md) | Medium | Self Join, Geometry |
| [618. Students Report By Geography](SQLs/leetcode/0618-students-report-by-geography/description.md) | Hard | Window Functions, Pivot Table |
| [1264. Page Recommendations](SQLs/leetcode/1264-page-recommendations/description.md) | Medium | Self Join, Union, Subquery |
| [1270. All People Report to the Given Manager](SQLs/leetcode/1270-all-people-report-to-the-given-manager/description.md) | Medium | Self Join, Hierarchical Query |
| [1280. Students and Examinations](SQLs/leetcode/1280-students-and-examinations/description.md) | Easy | Cross Join, Aggregation |
| [1336. Number of Transactions per Visit](SQLs/leetcode/1336-number-of-transactions-per-visit/description.md) | Hard | Recursive CTE, Aggregation |
| [1384. Total Sales Amount by Year](SQLs/leetcode/1384-total-sales-amount-by-year/description.md) | Hard | Recursive CTE, Date Manipulation |
| [1412. Find the Quiet Students in All Exams](SQLs/leetcode/1412-find-the-quiet-students-in-all-exams/description.md) | Hard | Window Functions, Ranking |
| [1440. Evaluate Boolean Expression](SQLs/leetcode/1440-evaluate-boolean-expression/description.md) | Medium | Self Join, CASE Expressions |
| [1445. Apples & Oranges](SQLs/leetcode/1445-apples-oranges/description.md) | Medium | Pivot Table, Aggregation, CASE Expressions |
| [1479. Sales by Day of the Week](SQLs/leetcode/1479-sales-by-day-of-the-week/description.md) | Hard | Pivot Table, Date Manipulation, CASE Expressions |
| [1635. Hopper Company Queries I](SQLs/leetcode/1635-hopper-company-queries-i/description.md) | Hard | Recursive CTE, Date Manipulation |
| [1645. Hopper Company Queries II](SQLs/leetcode/1645-hopper-company-queries-ii/description.md) | Hard | Recursive CTE, Date Manipulation, Pivot Table |
| [1651. Hopper Company Queries III](SQLs/leetcode/1651-hopper-company-queries-iii/description.md) | Hard | Recursive CTE, Window Functions, Moving Average |
| [1699. Number of Calls Between Two Persons](SQLs/leetcode/1699-number-of-calls-between-two-persons/description.md) | Medium | CASE Expressions, Aggregation |
| [1709. Biggest Window Between Visits](SQLs/leetcode/1709-biggest-window-between-visits/description.md) | Medium | Window Functions, Date Manipulation |
| [1767. Find the Subtasks That Did Not Execute](SQLs/leetcode/1767-find-the-subtasks-that-did-not-execute/description.md) | Hard | Recursive CTE |
| [1892. Page Recommendations II](SQLs/leetcode/1892-page-recommendations-ii/description.md) | Hard | Self Join, Union, Aggregation |
| [1917. Leetcodify Friends Recommendations](SQLs/leetcode/1917-leetcodify-friends-recommendations/description.md) | Hard | Self Join, Union, Date Manipulation, Aggregation |
| [1949. Strong Friendship](SQLs/leetcode/1949-strong-friendship/description.md) | Medium | Self Join, Union, Aggregation |
| [1972. First and Last Call On the Same Day](SQLs/leetcode/1972-first-and-last-call-on-the-same-day/description.md) | Hard | Window Functions, Union |
| [2004. The Number of Seniors and Juniors to Join the Company](SQLs/leetcode/2004-the-number-of-seniors-and-juniors-to-join-the-company/description.md) | Hard | Window Functions, Running Total |
| [2010. The Number of Seniors and Juniors to Join the Company II](SQLs/leetcode/2010-the-number-of-seniors-and-juniors-to-join-the-company-ii/description.md) | Hard | Window Functions, Running Total |
| [2142. The Number of Passengers in Each Bus I](SQLs/leetcode/2142-the-number-of-passengers-in-each-bus-i/description.md) | Medium | Self Join, Window Functions |
| [2153. The Number of Passengers in Each Bus II](SQLs/leetcode/2153-the-number-of-passengers-in-each-bus-ii/description.md) | Hard | Recursive CTE, Window Functions, Running Total |
| [2199. Finding the Topic of Each Post](SQLs/leetcode/2199-finding-the-topic-of-each-post/description.md) | Hard | String Manipulation, Self Join, Aggregation |
| [2362. Generate the Invoice](SQLs/leetcode/2362-generate-the-invoice/description.md) | Hard | Window Functions, Aggregation |
| [2394. Employees With Deductions](SQLs/leetcode/2394-employees-with-deductions/description.md) | Medium | Date Manipulation, Aggregation |
| [2474. Customers With Strictly Increasing Purchases](SQLs/leetcode/2474-customers-with-strictly-increasing-purchases/description.md) | Hard | Window Functions, Recursive CTE, Date Manipulation, Gaps & Islands |

### Other problems (non-LeetCode or modified)

| SQL Link | Level | Tags |
|---|---|---|
| [Exchange Seats (within Department)](SQLs/other_problems/exchange-seats-within-department/description.md) | Medium | Window Functions, CASE Expressions |

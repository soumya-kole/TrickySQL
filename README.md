# TRICKY SQL

This repository contains tricky and advanced SQL problems frequently asked in job interviews, solved in MySQL. Problems under `SQLs/leetcode/` and `SQLs/other_problems/` live one-per-folder, split across `description.md`, `setup.md`, and `solutions.md` — see [Problem file structure](#problem-file-structure). `Meta/` (a separate corpus of Meta Data Engineering interview problems) instead uses a single combined `.md` file per problem.

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

Problems under `SQLs/leetcode/` and `SQLs/other_problems/` live one-per-folder, each containing:

- `description.md` — the problem statement and examples
- `setup.md` — the `## Setup` (and optional `## Setup2`, …) `sql` block(s)
- `solutions.md` — one or more named solutions, each in its own `sql` block

`SQLs/leetcode/` folders are named `<zero-padded LeetCode number>-<kebab-case-title>` (e.g. `2142-the-number-of-passengers-in-each-bus-i`); `SQLs/other_problems/` folders (non-LeetCode or modified problems) are named `<kebab-case-title>` (e.g. `exchange-seats-within-department`).

`Meta/` problems instead follow a single-file layout (`## Description`, `## Setup`, `## Solutions`, and optional `## Setup2`, `## Setup3`, … sections for alternative datasets).

## Loading problem data

Use `make setup` to load a problem's data into the running MySQL instance.

```bash
# SQLs/leetcode/ and SQLs/other_problems/ problems — by problem folder name
make setup 2142-the-number-of-passengers-in-each-bus-i
make setup exchange-seats-within-department

# A single-file general problem (e.g. under Meta/) — by filename (searches all
# subdirectories automatically) or by relative path
make setup My_Problem.md
make setup Meta/My_Problem.md
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

4. Add a row for it to the **LeetCode problems** table in the [SQLs](#sqls) section below, keeping the table sorted by problem number.

**Other (non-LeetCode or modified) problem:**

1. Create `SQLs/other_problems/<kebab-case-title>/` with `description.md`, `setup.md`, and `solutions.md`, same structure and rules as the LeetCode case (no number prefix).
2. Verify the data loads cleanly before committing:

   ```bash
   make setup <kebab-case-title>
   ```

3. Add a row for it to the **Other problems** table in the [SQLs](#sqls) section below.

Each table row needs a **SQL Link** (`description.md` inside the problem folder), a **Level** (for LeetCode problems, use the problem's real LeetCode difficulty rather than guessing), and one or more **Tags** describing the SQL techniques the solution uses (e.g. `Recursive CTE`, `Window Functions`, `Pivot Table`).

A pre-commit hook (enabled via `make install-hooks`, see [Prerequisite](#prerequisite)) blocks commits that add a problem under `SQLs/` without a matching link somewhere in this README — but it only checks that a link exists, not that Level/Tags are correct, so don't rely on it in place of adding the full row.

## SQLs

### LeetCode problems

| SQL Link | Level | Tags |
|---|---|---|
| [180. Consecutive Numbers](SQLs/leetcode/0180-consecutive-numbers/description.md) | Medium | Window Functions, Gaps & Islands |
| [197. Rising Temperature](SQLs/leetcode/0197-rising-temperature/description.md) | Easy | Self Join, Window Functions, Date Manipulation |
| [534. Game Play Analysis III](SQLs/leetcode/0534-game-play-analysis-iii/description.md) | Medium | Window Functions, Self Join, Running Total |
| [550. Game Play Analysis IV](SQLs/leetcode/0550-game-play-analysis-iv/description.md) | Medium | Self Join, Date Manipulation, Aggregation |
| [569. Median Employee Salary](SQLs/leetcode/0569-median-employee-salary/description.md) | Hard | Window Functions, Median |
| [571. Find Median Given Frequency of Numbers](SQLs/leetcode/0571-find-median-given-frequency-of-numbers/description.md) | Hard | Recursive CTE, Window Functions, Median |
| [579. Find Cumulative Salary of an Employee](SQLs/leetcode/0579-find-cumulative-salary-of-an-employee/description.md) | Hard | Window Functions, Ranking, Running Total |
| [603. Consecutive Available Seats](SQLs/leetcode/0603-consecutive-available-seats/description.md) | Easy | Self Join, Window Functions, Gaps & Islands |
| [612. Shortest Distance in a Plane](SQLs/leetcode/0612-shortest-distance-in-a-plane/description.md) | Medium | Self Join, Geometry |
| [618. Students Report By Geography](SQLs/leetcode/0618-students-report-by-geography/description.md) | Hard | Window Functions, Pivot Table |
| [1097. Game Play Analysis V](SQLs/leetcode/1097-game-play-analysis-v/description.md) | Hard | Window Functions, Date Manipulation, Aggregation |
| [1225. Report Contiguous Dates](SQLs/leetcode/1225-report-contiguous-dates/description.md) | Hard | Union, Window Functions, Gaps & Islands |
| [1264. Page Recommendations](SQLs/leetcode/1264-page-recommendations/description.md) | Medium | Self Join, Union, Subquery |
| [1270. All People Report to the Given Manager](SQLs/leetcode/1270-all-people-report-to-the-given-manager/description.md) | Medium | Self Join, Hierarchical Query |
| [1280. Students and Examinations](SQLs/leetcode/1280-students-and-examinations/description.md) | Easy | Cross Join, Aggregation |
| [1336. Number of Transactions per Visit](SQLs/leetcode/1336-number-of-transactions-per-visit/description.md) | Hard | Recursive CTE, Aggregation |
| [1369. Get the Second Most Recent Activity](SQLs/leetcode/1369-get-the-second-most-recent-activity/description.md) | Hard | Window Functions, Ranking |
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
| [2173. Longest Winning Streak](SQLs/leetcode/2173-longest-winning-streak/description.md) | Hard | Gaps & Islands, Window Functions |
| [2199. Finding the Topic of Each Post](SQLs/leetcode/2199-finding-the-topic-of-each-post/description.md) | Hard | String Manipulation, Self Join, Aggregation |
| [2362. Generate the Invoice](SQLs/leetcode/2362-generate-the-invoice/description.md) | Hard | Window Functions, Aggregation |
| [2394. Employees With Deductions](SQLs/leetcode/2394-employees-with-deductions/description.md) | Medium | Date Manipulation, Aggregation |
| [2474. Customers With Strictly Increasing Purchases](SQLs/leetcode/2474-customers-with-strictly-increasing-purchases/description.md) | Hard | Window Functions, Recursive CTE, Date Manipulation, Gaps & Islands |

### Other problems (non-LeetCode or modified)

| SQL Link | Level | Tags |
|---|---|---|
| [Explode Implementation](SQLs/other_problems/explode-implementation/description.md) | Medium | Recursive CTE, String Manipulation |
| [Hierarchical Query in MySQL (CONNECT BY equivalent)](SQLs/other_problems/connect-by-hierarchical-query/description.md) | Medium | Recursive CTE, Hierarchical Query |
| [Paired Products (Frequently Bought Together)](SQLs/other_problems/paired-products-frequently-bought-together/description.md) | Medium | Self Join, Aggregation, Top-N |
| [Exchange Seats (within Department)](SQLs/other_problems/exchange-seats-within-department/description.md) | Medium | Window Functions, CASE Expressions |
| [Match Win/Loss Summary](SQLs/other_problems/match-win-summary/description.md) | Easy | Union, Aggregation, CASE Expressions |
| [Split Full Name into First/Middle/Last](SQLs/other_problems/first-middle-last-name/description.md) | Easy | String Manipulation, CASE Expressions |
| [Start and End Location of a Trip](SQLs/other_problems/start-end-location-of-a-trip/description.md) | Medium | Anti Join, Aggregation, CASE Expressions |

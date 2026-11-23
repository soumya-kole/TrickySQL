# 1225. Report Contiguous Dates - Solutions

## Solution 1: Union + gaps-and-islands via difference of two `RANK()`s

`all_runs` unions both tables into one 2019 timeline, tagging each date with
its state. `cte2` then takes the difference of two ranks:

- `RANK() OVER (ORDER BY run_date)`: the row's position in the whole timeline.
- `RANK() OVER (PARTITION BY status ORDER BY run_date)`: its position among
  rows with the same state.

Inside a run of consecutive same-state days both ranks climb by one together,
so the difference (`rnk`) stays constant. It only changes once days of the
other state come in between. This compares row positions rather than calendar
dates, so it relies on the task running **every day**; a missing date would
not break an island.

`rnk` is only unique *within* a state, so `GROUP BY` needs `status` as well.
For `failed` on 01-01, `succeeded` on 01-02 and `failed` on 01-03:

| run_date   | status    | overall rank | rank in status | rnk |
| ---------- | --------- | ------------ | -------------- | --- |
| 2019-01-01 | failed    | 1            | 1              | 0   |
| 2019-01-02 | succeeded | 2            | 1              | 1   |
| 2019-01-03 | failed    | 3            | 2              | 1   |

Grouping by `rnk` alone would merge the last two rows into one interval. Load
this dataset with `make setup 1225-report-contiguous-dates 2`.

#### MySQL

```sql
WITH
    all_runs AS (
        SELECT 'failed' AS status, fail_date AS run_date
        FROM Failed
        WHERE fail_date BETWEEN '2019-01-01' AND '2019-12-31'

        UNION

        SELECT 'succeeded' AS status, success_date AS run_date
        FROM Succeeded
        WHERE success_date BETWEEN '2019-01-01' AND '2019-12-31'
    ),
    cte2 AS (
        SELECT
            status,
            run_date,
            RANK() OVER (ORDER BY run_date)
                - RANK() OVER (PARTITION BY status ORDER BY run_date) AS rnk
        FROM all_runs
    )
SELECT
    status AS period_state,
    MIN(run_date) AS start_date,
    MAX(run_date) AS end_date
FROM cte2
GROUP BY status, rnk
ORDER BY start_date;
```

## Solution 2: Union + gaps-and-islands via `dt - RANK()`

`Failed` and `Succeeded` are two separate tables, but the report needs one
timeline of contiguous ranges. `T` unions them into a single `(dt, st)`
stream, filtered to 2019, so every day in range appears exactly once tagged
with its state.

From there it's the classic gaps-and-islands trick: `RANK()` (partitioned by
`st`, ordered by `dt`) gives each row its rank within same-state rows, and
`SUBDATE(dt, rnk)` (`grp`) subtracts that rank off the date. Within a run of
*consecutive* calendar days sharing the same `st`, `dt` and `rnk` climb by one
together, so `grp` stays constant for the whole run — a change in `grp` marks
a new island. `RANK()` rather than `ROW_NUMBER()` is really just a style
choice here: both `fail_date` and `success_date` are primary keys, so there
are no ties within a partition for `RANK()` to handle differently.

`GROUP BY grp, period_state` then buckets each island together, and
`MIN(dt)`/`MAX(dt)` read off its `start_date`/`end_date`.

#### MySQL

```sql
WITH
    T AS (
        SELECT fail_date AS dt, 'failed' AS st
        FROM Failed
        WHERE YEAR(fail_date) = 2019

        UNION ALL

        SELECT success_date AS dt, 'succeeded' AS st
        FROM Succeeded
        WHERE YEAR(success_date) = 2019
    ),
    T1 AS (
        SELECT
            *,
            RANK() OVER (PARTITION BY st ORDER BY dt) AS rnk
        FROM T
    ),
    T2 AS (
        SELECT *, SUBDATE(dt, rnk) AS grp
        FROM T1
    )
SELECT
    st AS period_state,
    MIN(dt) AS start_date,
    MAX(dt) AS end_date
FROM T2
GROUP BY grp, period_state
ORDER BY start_date;
```

`SUBDATE(dt, rnk)` uses the plain-integer form of `SUBDATE` (`rnk` days back
from `dt`, no `INTERVAL` needed) — see
[Date_Functions.md](../../../Concepts/Date_Functions.md) for why `DATE_SUB`
can't do this same shorthand.

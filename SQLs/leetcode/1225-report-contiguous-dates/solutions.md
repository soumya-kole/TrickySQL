# 1225. Report Contiguous Dates - Solutions

## Solution 1: Union + gaps-and-islands via `dt - RANK()`

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

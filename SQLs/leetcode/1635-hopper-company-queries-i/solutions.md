# 1635. Hopper Company Queries I - Solutions

## Solution 1

Build the month scaffold `M` (1–12) with a recursive CTE, since every month must
appear in the output even with zero accepted rides. `D` collapses each driver's
active month to `1` if they joined before 2020 (they were already active for all of
2020) or to their actual join month otherwise, so "active by end of month" reduces to
a simple `M.month >= D.join_month` comparison. `R` pre-aggregates accepted-ride counts
per month so the final join is one-to-one instead of fanning out per ride.

```sql
SELECT
    M.month,
    COUNT(DISTINCT D.driver_id),
    COALESCE(R.cnt, 0)
FROM M
LEFT JOIN D ON M.month >= D.join_month
LEFT JOIN R ON M.month = R.requested_month
GROUP BY 1, 3
ORDER BY 1;
```

also works, but `GROUP BY M.month` with `MAX(R.cnt)` (below) is more idiomatic —
it states the real intent ("one ride count per month") explicitly through the
aggregate, rather than relying on a reader to work out why grouping by a derived,
positionally-referenced column is safe.

#### MySQL

```sql
WITH RECURSIVE
    M AS (
        SELECT 1 AS month
        UNION ALL
        SELECT month + 1
        FROM M
        WHERE month < 12
    ),
    D AS (
        SELECT
            driver_id,
            CASE
                WHEN YEAR(join_date) < 2020 THEN 1
                ELSE MONTH(join_date)
            END AS join_month
        FROM Drivers
        WHERE YEAR(join_date) <= 2020
    ),
    R AS (
        SELECT
            COUNT(r.ride_id) AS cnt,
            MONTH(r.requested_at) AS requested_month
        FROM Rides AS r
        JOIN AcceptedRides AS ar ON r.ride_id = ar.ride_id AND YEAR(r.requested_at) = 2020
        GROUP BY MONTH(r.requested_at)
    )
SELECT
    M.month,
    COUNT(DISTINCT D.driver_id) AS active_drivers,
    COALESCE(MAX(R.cnt), 0)     AS accepted_rides
FROM M
LEFT JOIN D ON M.month >= D.join_month
LEFT JOIN R ON M.month = R.requested_month
GROUP BY M.month
ORDER BY M.month;
```

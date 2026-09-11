# 1645. Hopper Company Queries II - Solutions

## Solution 1

`M` is the month scaffold (1–12), needed because every month must appear in the
output even with `0` working drivers. `D` collapses each driver's active month to
`1` if they joined before 2020, or to their actual join month otherwise, so
`active_drivers` reduces to a simple `M.month >= D.joining_month` range join,
grouped by month.

`valid_rides` inner-joins `Rides` to `AcceptedRides` — filtered to
`YEAR(requested_at) = 2020` — *before* joining that pair to `M`. Doing the inner
join first means an unaccepted ride, or a ride accepted in a different year,
never produces a row to begin with; joining `AcceptedRides` separately with a
`LEFT JOIN` would let those rows survive (as NULL-decorated matches) and get
counted anyway, and matching purely on `MONTH(requested_at)` without pinning the
year would also pull in rides from other years that happen to share a month
number.

The count itself is `COUNT(DISTINCT ar.driver_id)`, not `COUNT(ar.ride_id)`. The
question asks for the *percentage of drivers* who worked that month, not the
*number of accepted rides* — a driver with two accepted rides in the same month
is still one working driver, so counting rides would overstate the percentage
(and could push it past what the ride/driver ratio should allow) whenever a
driver has more than one accepted ride in a given month.

Finally, `COALESCE(ROUND(v.driver_cnt * 100 / a.joined, 2), 0)` handles the
"zero active drivers" edge case the problem calls out explicitly. `a.joined` is
never `NULL` (`COUNT()` returns `0`, not `NULL`, when nothing matches), but
dividing by that `0` still evaluates to `NULL` in MySQL regardless — division by
zero yields `NULL`, not an error, independent of whether the operands
themselves are `NULL`. `COALESCE` turns that `NULL` back into the `0` the
problem requires.

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
            END AS joining_month
        FROM Drivers
        WHERE YEAR(join_date) < 2021
    ),
    active_drivers AS (
        SELECT
            M.month,
            COUNT(driver_id) AS joined
        FROM M
        LEFT JOIN D ON M.month >= D.joining_month
        GROUP BY M.month
    ),
    valid_rides AS (
        SELECT
            M.month AS ride_month,
            COUNT(DISTINCT ar.driver_id) AS driver_cnt
        FROM M
        LEFT JOIN (
            Rides r
            JOIN AcceptedRides ar
                ON r.ride_id = ar.ride_id
                AND YEAR(r.requested_at) = 2020
        ) ON M.month = MONTH(r.requested_at)
        GROUP BY 1
    )
SELECT
    a.month,
    COALESCE(ROUND(v.driver_cnt * 100 / a.joined, 2), 0) AS working_percentage
FROM valid_rides v
JOIN active_drivers a ON a.month = v.ride_month
ORDER BY a.month;
```

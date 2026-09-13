# 1651. Hopper Company Queries III - Solutions

## Solution 1

`Months` is the same 1–12 scaffold used in the earlier Hopper Company Queries
problems, needed because every month must appear in the output even with `0`
rides. `Ride` left-joins `Rides` (filtered to `YEAR(requested_at) = 2020`
inline on the join, not in a `WHERE`) and then `AcceptedRides`, so a month
with no rides at all, or with rides that were never accepted, still produces
a row — just with `NULL` distance/duration — rather than disappearing. Using
a `WHERE` clause instead of pushing the year filter into the `ON` condition
would turn the `LEFT JOIN` back into an inner join in effect, dropping
month rows that have no 2020 match. `SUM(IFNULL(ride_distance, 0))` then
collapses those `NULL`s to `0` per month, which is what the problem's
worked example expects (e.g. January's total distance is `63`, from the
one accepted ride in March counted three windows later, not `NULL`).

The 3-month rolling window itself is `AVG(...) OVER (ROWS BETWEEN CURRENT ROW
AND 2 FOLLOWING)`, ordered implicitly by `Ride`'s row order (`month` is
already 1–12 in sequence from the CTE). This computes, for each starting
month, the average of that month and the two after it — exactly the
"3-month window starting from month N" the problem asks for. Averaging
inside the window function rather than summing-then-dividing-by-3 avoids a
separate arithmetic step, and it also means a window with fewer than 3 rows
would still average correctly (though that never happens here, because...).

The final `LIMIT 10` is what keeps only months 1–10 as valid window starts.
Months 11 and 12 would produce windows with fewer than three months of
2020 data behind their `ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING` frame (the
frame would run past month 12 with nothing there), so the recursive CTE
still generates rows for them, but they're excluded from the final result
since the problem only wants windows through "October - December 2020".

#### MySQL

```sql
WITH RECURSIVE
    Months AS (
        SELECT 1 AS month
        UNION ALL
        SELECT month + 1
        FROM Months
        WHERE month < 12
    ),
    Ride AS (
        SELECT
            month,
            SUM(IFNULL(ride_distance, 0)) AS ride_distance,
            SUM(IFNULL(ride_duration, 0)) AS ride_duration
        FROM
            Months AS m
            LEFT JOIN Rides AS r ON month = MONTH(requested_at) AND YEAR(requested_at) = 2020
            LEFT JOIN AcceptedRides AS a ON r.ride_id = a.ride_id
        GROUP BY month
    )
SELECT
    month,
    ROUND(
        AVG(ride_distance) OVER (ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING),
        2
    ) AS average_ride_distance,
    ROUND(
        AVG(ride_duration) OVER (ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING),
        2
    ) AS average_ride_duration
FROM Ride
ORDER BY month
LIMIT 10;
```

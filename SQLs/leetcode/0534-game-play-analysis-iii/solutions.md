# 534. Game Play Analysis III - Solutions

## Solution 1: Running sum with a window function

Each row needs the total games played by that player up to and including its own date. `SUM(games_played) OVER (PARTITION BY player_id ORDER BY event_date)` computes exactly that running total, partitioned per player and ordered by date, in a single pass over the table.

#### MySQL

```sql
SELECT
    player_id,
    event_date,
    SUM(games_played) OVER (
        PARTITION BY player_id
        ORDER BY event_date
    ) AS games_played_so_far
FROM Activity;
```

Omitting an explicit frame here is equivalent to writing `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (MySQL's default frame for an aggregate window function once `ORDER BY` is present), not `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. The two only differ when the `ORDER BY` column has ties: `RANGE` gives every peer row (same `event_date`) the combined total of the whole peer group, while `ROWS` sums strictly by physical row position. Since `(player_id, event_date)` is the primary key, no ties are possible within a partition, so `ROWS` would produce the identical result and can be used interchangeably here.

Contrast this with [579. Find Cumulative Salary of an Employee](../0579-find-cumulative-salary-of-an-employee/solutions.md), where `RANGE` is not interchangeable with `ROWS`: there the `ORDER BY` column (`month`) can have gaps between consecutive rows for the same employee, so `RANGE BETWEEN 2 PRECEDING AND CURRENT ROW` (which looks at the `month` *value*) and `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` (which looks at physical row position) genuinely diverge.

## Solution 2: Self-join on prior dates

Join `Activity` to itself on matching `player_id` where the second copy's date is on or before the first copy's date, then group by the first copy's `player_id` and `event_date` and sum the matched `games_played`. This reproduces the window function's running total without relying on `OVER()`.

#### MySQL

```sql
SELECT
    t1.player_id,
    t1.event_date,
    SUM(t2.games_played) AS games_played_so_far
FROM Activity t1
JOIN Activity t2
    ON t1.player_id = t2.player_id
    AND t2.event_date <= t1.event_date
GROUP BY t1.player_id, t1.event_date;
```

# 550. Game Play Analysis IV - Solutions

## Solution 1: First-login CTE with a self left join

A CTE first reduces `Activity` to one row per player, `m_e`, their minimum (first) `event_date`. Left joining that back to `Activity` on matching `player_id` and `DATEDIFF(a.event_date, c.m_e) = 1` finds, per player, the row for the day right after their first login — if one exists. Because the CTE already has exactly one row per player, the join produces exactly one output row per player too: `a.event_date IS NOT NULL` when a next-day login was found (retained), `NULL` when the left join found nothing (not retained). `AVG()` over these one-row-per-player booleans is directly the fraction retained — no separate distinct-count denominator needed.

#### MySQL

```sql
WITH cte AS (
    SELECT
        player_id,
        MIN(event_date) AS m_e
    FROM Activity
    GROUP BY 1
)
SELECT ROUND(AVG(a.event_date IS NOT NULL), 2) AS fraction
FROM cte c
LEFT JOIN Activity a
    ON a.player_id = c.player_id
    AND DATEDIFF(a.event_date, c.m_e) = 1;
```

## Solution 2: Window function, collapsed to one row per player, then AVG

The innermost subquery tags every login with `activity_gap`, the number of days since that player's first login (via `MIN(event_date) OVER (PARTITION BY player_id)`). The middle subquery then collapses each player down to a single row with `GROUP BY player_id`, using `MAX(CASE WHEN activity_gap = 1 THEN 1 ELSE 0 END)` to record whether *any* of that player's logins landed exactly one day after their first (an "OR across the group"). With exactly one row per player at that point, `AVG(retained)` in the outer query is the fraction directly.

#### MySQL

```sql
SELECT ROUND(AVG(retained), 2) AS fraction
FROM (
    SELECT
        player_id,
        MAX(CASE WHEN activity_gap = 1 THEN 1 ELSE 0 END) AS retained
    FROM (
        SELECT
            player_id,
            DATEDIFF(
                event_date,
                MIN(event_date) OVER (PARTITION BY player_id)
            ) AS activity_gap
        FROM Activity
    ) t
    GROUP BY player_id
) p;
```

## Solution 3: Window function, ratio of distinct-player counts

For each row, `MIN(event_date) OVER (PARTITION BY player_id)` gives that player's first login date, and `DATEDIFF` against the current row's date tells how many days later it is. A player retained on day 2 has some row where that gap equals `1`. Counting distinct players with a `1`-day gap and dividing by the count of distinct players gives the fraction; `CASE WHEN ... END` inside `COUNT(DISTINCT ...)` keeps only the retained players in the numerator. Unlike Solutions 1 and 2, this works directly on the per-login rows without first collapsing to one row per player, since the numerator and denominator each explicitly count distinct `player_id`s rather than relying on row count.

#### MySQL

```sql
SELECT
    ROUND(
        COUNT(DISTINCT CASE WHEN activity_gap = 1 THEN player_id END) /
        COUNT(DISTINCT player_id)
    , 2) AS fraction
FROM (
    SELECT
        player_id,
        event_date,
        DATEDIFF(
            event_date,
            MIN(event_date) OVER (PARTITION BY player_id)
        ) AS activity_gap
    FROM Activity
) tbl;
```

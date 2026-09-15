# 1097. Game Play Analysis V - Solutions

## Solution 1: First-login CTE with a self left join

A CTE first reduces `Activity` to one row per player, `install_dt`, their minimum (first) `event_date`. Left joining that back to `Activity` on matching `player_id` and `DATEDIFF(install_dt, event_date) = -1` (i.e. `event_date` is exactly one day after `install_dt`) finds, per player, the row for the day right after their install — if one exists. Because the CTE already has exactly one row per player, and `(player_id, event_date)` is the table's primary key, the join matches at most one row per player, so the result still has exactly one row per player: `event_date IS NOT NULL` when a next-day login was found (retained), `NULL` otherwise. Grouping by `install_dt` and averaging the retained flag gives `Day1_retention` directly; `COUNT(DISTINCT player_id)` gives `installs`.

`DISTINCT` isn't strictly required in `COUNT(DISTINCT player_id)` here — since each player contributes exactly one row per group (no fan-out from the join), `COUNT(player_id)` would return the same result. It's kept for clarity, making the "one row per player" intent explicit.

#### MySQL

```sql
WITH cte AS (
    SELECT
        player_id,
        MIN(event_date) AS install_dt
    FROM Activity
    GROUP BY player_id
),
cte2 AS (
    SELECT
        m.install_dt,
        m.player_id,
        a.event_date
    FROM cte m
    LEFT JOIN Activity a
        ON m.player_id = a.player_id
        AND DATEDIFF(m.install_dt, a.event_date) = -1
)
SELECT
    install_dt,
    COUNT(DISTINCT player_id) AS installs,
    ROUND(AVG(CASE WHEN event_date IS NOT NULL THEN 1 ELSE 0 END), 2) AS Day1_retention
FROM cte2
GROUP BY 1;
```

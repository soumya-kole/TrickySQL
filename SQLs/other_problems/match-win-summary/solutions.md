# Match Win/Loss Summary - Solutions

## Solution 1: Union both team columns, then aggregate

Each match contributes one row per team: `Team_1` and `Team_2` are unioned into a single `team` column, with a `CASE` flag marking whether that team was the `Winner` of the match. Once every team's matches are stacked into one column, a simple `GROUP BY` counts total matches played and sums the win flag to get wins/losses.

#### MySQL

```sql
WITH all_matches AS (
    SELECT
        Team_1 AS team,
        CASE
            WHEN Team_1 = Winner THEN 1
            ELSE 0
        END AS win_flag
    FROM icc_world_cup
    UNION ALL
    SELECT
        Team_2 AS team,
        CASE
            WHEN Team_2 = Winner THEN 1
            ELSE 0
        END AS win_flag
    FROM icc_world_cup
)
SELECT
    team,
    COUNT(*) AS total_matches,
    SUM(win_flag) AS no_of_win,
    COUNT(*) - SUM(win_flag) AS no_of_loses
FROM all_matches
GROUP BY team
ORDER BY no_of_win DESC, total_matches;
```

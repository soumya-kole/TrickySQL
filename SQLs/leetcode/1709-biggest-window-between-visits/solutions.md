# 1709. Biggest Window Between Visits - Solutions

## Solution 1: `LEAD` to pair each visit with the next one

Each "window" is the gap between one visit and the next visit by the same user, with the very last visit paired against today (`2021-01-01`) instead of a real next visit. `LEAD(visit_date, 1, '2021-01-01') OVER (PARTITION BY user_id ORDER BY visit_date)` gives exactly that: the next chronological visit for the same user, or the default date when there isn't one. `DATEDIFF` turns each pair into a day count, and `MAX` per user picks out the biggest window.

#### MySQL

```sql
WITH gaps AS (
    SELECT
        user_id,
        DATEDIFF(
            LEAD(visit_date, 1, '2021-01-01') OVER (PARTITION BY user_id ORDER BY visit_date),
            visit_date
        ) AS window_days
    FROM UserVisits
)
SELECT user_id, MAX(window_days) AS biggest_window
FROM gaps
GROUP BY user_id
ORDER BY user_id;
```

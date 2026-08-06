# Exchange Seats (within Department) - Solutions

## Solution 1: Window `COUNT` per department, then swap by parity

Compute how many seats exist in each department, then for every row: if `id` is odd and not the last seat, swap forward (`id + 1`); if `id` is odd and is the last (odd-count) seat, keep it; otherwise swap backward (`id - 1`).

#### MySQL

```sql
WITH cte AS (
    SELECT
        *,
        COUNT(*) OVER (PARTITION BY dept) AS cnt
    FROM Seat
)
SELECT
    dept,
    CASE
        WHEN id % 2 = 1 AND id < cnt THEN id + 1
        WHEN id % 2 = 1 AND id = cnt THEN id
        ELSE id - 1
    END AS id,
    student
FROM cte
ORDER BY dept, id;
```

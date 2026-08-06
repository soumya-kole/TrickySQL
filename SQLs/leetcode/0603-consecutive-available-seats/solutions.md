# 603. Consecutive Available Seats - Solutions

## Solution 1: Self-Join

Join `Cinema` with itself on adjacent `seat_id`s (`ABS(a.seat_id - b.seat_id) = 1`), keeping only pairs where both seats are free. Every seat_id that appears in such a pair has at least one free neighbor, so it's part of a consecutive run.

`DISTINCT` is required because a seat with free neighbors on **both** sides matches the join twice (once as `b.seat_id = a.seat_id - 1`, once as `b.seat_id = a.seat_id + 1`), which would otherwise duplicate its `a.seat_id` in the result.

#### MySQL

```sql
SELECT DISTINCT a.seat_id
FROM Cinema a
JOIN Cinema b ON ABS(a.seat_id - b.seat_id) = 1 AND a.free AND b.free
ORDER BY 1;
```

## Solution 2: LAG / LEAD

For each seat, add `free` to its previous seat's `free` (`LAG`) and to its next seat's `free` (`LEAD`). A seat is part of a consecutive pair if either sum equals 2, meaning that seat and its neighbor are both free.

#### MySQL

```sql
WITH cte AS (
    SELECT
        seat_id,
        free + LAG(free) OVER (ORDER BY seat_id) AS prev_pair,
        free + LEAD(free) OVER (ORDER BY seat_id) AS next_pair
    FROM Cinema
)
SELECT seat_id
FROM cte
WHERE prev_pair = 2 OR next_pair = 2
ORDER BY 1;
```

## Solution 3: Sliding Window Sum

For each seat, count how many free seats fall within a 3-row window centered on it (`1 PRECEDING` to `1 FOLLOWING`). A free seat with more than one free seat in its window must have a free neighbor.

#### MySQL

```sql
WITH cte AS (
    SELECT
        seat_id,
        free,
        SUM(free = 1) OVER (
            ORDER BY seat_id
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
        ) AS free_neighbors
    FROM Cinema
)
SELECT seat_id
FROM cte
WHERE free = 1 AND free_neighbors > 1
ORDER BY 1;
```

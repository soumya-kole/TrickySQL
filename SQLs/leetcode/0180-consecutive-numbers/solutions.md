# 180. Consecutive Numbers - Solutions

## Solution 1: `LAG`/`LEAD` to check both neighbors

`LAG`/`LEAD` (ordered by `id`) give each row its previous and next `num`. A row
matches `num = p_n AND num = n_n` exactly when it sits in the *middle* of a run
of three identical consecutive values, so any run of three or more always
produces at least one matching row. `DISTINCT` then collapses that down to one
row per qualifying number.

#### MySQL

```sql
WITH cte AS (
    SELECT
        id,
        num,
        LAG(num, 1)  OVER (ORDER BY id) AS p_n,
        LEAD(num, 1) OVER (ORDER BY id) AS n_n
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM cte
WHERE num = p_n AND num = n_n;
```

`LAG`/`LEAD` only care about relative row order from `ORDER BY id`, not the
numeric gap between `id` values — a deleted row that leaves `id` jumping from,
say, 2 straight to 4 doesn't break this query, since the remaining rows are
still adjacent in `id` order and get compared as neighbors correctly. See
[Window_Function_Anatomy.md](../../../Concepts/Window_Function_Anatomy.md)
for why `LAG`/`LEAD` ignore frame clauses entirely (Step 6) and what can go
wrong with them.

## Solution 2: Gaps-and-islands via `id - ROW_NUMBER()`

Sort by `(num, id)` and subtract a running `ROW_NUMBER()` from `id`. Within a
run of rows that share the same `num` and whose `id`s increase one at a time,
`id` and the row number climb in lockstep, so `id - ROW_NUMBER()` (`grp`) stays
constant — a classic "gaps and islands" trick. `GROUP BY num, grp` then buckets
each such run together, and `HAVING COUNT(*) > 2` keeps only runs of three or
more.

The `ROW_NUMBER()` isn't partitioned by `num`, so its running count carries
over from the `num = 1` block into the `num = 2` block — but that's harmless:
`GROUP BY num, grp` only checks whether `grp` matches *within* the same `num`,
so the shared numeric offset between different `num` groups never causes a
false merge.

#### MySQL

```sql
WITH cte AS (
    SELECT
        num,
        id,
        id * 1.0 - (ROW_NUMBER() OVER (ORDER BY num, id)) * 1.0 AS grp
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM cte
GROUP BY num, grp
HAVING COUNT(*) > 2;
```

The `* 1.0` on both sides isn't stylistic — `ROW_NUMBER()` returns `BIGINT
UNSIGNED`, and `id - ROW_NUMBER()` can go negative (it does here, for the
`num = 2` block). Subtracting into a negative result under unsigned integer
arithmetic throws `BIGINT UNSIGNED value is out of range` in MySQL. Multiplying
both operands by the decimal literal `1.0` forces the subtraction to happen in
`DECIMAL` instead, which has no such unsigned-only representation.

Unlike Solution 1, this one *does* depend on `id` being gapless: it detects a
run by checking that `id` climbs by exactly 1 per row, not just that the rows
are adjacent in `id` order. With `id` values `1, 2, 4, 5` all sharing the same
`num` (row `id = 3` deleted, but the remaining four rows are still genuinely
adjacent), this technique splits them into two groups of 2 (`{1,2}` and
`{4,5}`) and misses the run entirely, while Solution 1 still finds it. That
gap can't happen here — the problem guarantees `id` is a gapless autoincrement
starting from 1 — but it's the reason to reach for `LAG`/`LEAD` instead if
that guarantee ever doesn't hold.

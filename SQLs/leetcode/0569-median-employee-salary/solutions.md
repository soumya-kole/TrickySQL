# 569. Median Employee Salary - Solutions

## Solution 1: Rank within each company, then keep the middle position(s)

1. `ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary)` ranks each employee's salary within their own company, breaking ties by `id` (rows come out of `Employee` ordered by `id`, so equal salaries keep ascending `id` order).
2. `COUNT(id) OVER (PARTITION BY company)` gives each row the company's total headcount, `cnt`.
3. The median position(s) are exactly the rows with `cnt/2 <= rn <= cnt/2 + 1`. Because MySQL's `/` is decimal division, one predicate covers both parities: for an **even** `cnt` the two bounds land on whole numbers, keeping the two middle rows; for an **odd** `cnt` they land on `.5`, keeping the single middle row.

#### MySQL

```sql
WITH cte AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary) AS rn,
        COUNT(id)    OVER (PARTITION BY company)                 AS cnt
    FROM Employee
)
SELECT
    id,
    company,
    salary
FROM cte
WHERE rn BETWEEN cnt / 2 AND cnt / 2 + 1;
```

> For company A (`cnt = 6`, even) the predicate keeps `rn` 3 and 4 — ids 5 and 6. For company C (`cnt = 5`, odd) it keeps only `rn = 3` — id 14. This matches the example's expected output.

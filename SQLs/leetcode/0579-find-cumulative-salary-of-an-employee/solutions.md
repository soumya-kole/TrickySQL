# 579. Find Cumulative Salary of an Employee - Solutions

Both solutions below build the same 3-month sum with:

```sql
SUM(salary) OVER (
    PARTITION BY id
    ORDER BY month
    RANGE BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

`RANGE` (not `ROWS`) is what makes this correct: months are not always consecutive rows
(e.g. employee 1 has no data for months 5 and 6), so `ROWS BETWEEN 2 PRECEDING AND
CURRENT ROW` would wrongly pull in the 2 preceding *rows* regardless of how far back in
time they are. `RANGE BETWEEN 2 PRECEDING AND CURRENT ROW` instead looks at the `month`
*value* itself, so month 7's window only reaches back to month 5 — finding nothing there
— and correctly sums to just its own salary. See
[Concepts/Window_Function_Anatomy.md, section 5f](../../../Concepts/Window_Function_Anatomy.md#5f-range-with-a-value-offset-when-a-row-count-window-is-wrong)
for a worked example of this exact `RANGE` vs `ROWS` gap.

They only differ in how they drop each employee's most recent month.

## Solution 1: `RANK` over month descending

Rank each employee's months newest-first with `RANK() OVER (PARTITION BY id ORDER BY
month DESC)` — the most recent month always gets rank `1` — then keep only `rk > 1`.

#### MySQL

```sql
WITH cumulative AS (
    SELECT
        id,
        month,
        SUM(salary) OVER (
            PARTITION BY id
            ORDER BY month
            RANGE BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS Salary,
        RANK() OVER (
            PARTITION BY id
            ORDER BY month DESC
        ) AS rk
    FROM Employee
)
SELECT id, month, Salary
FROM cumulative
WHERE rk > 1
ORDER BY id, month DESC;
```

## Solution 2: `NOT IN` against each employee's max month

Compute `(id, MAX(month))` for every employee and exclude those pairs directly with
`NOT IN`, then apply the same windowed sum.

#### MySQL

```sql
SELECT
    id,
    month,
    SUM(salary) OVER (
        PARTITION BY id
        ORDER BY month
        RANGE BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS Salary
FROM Employee
WHERE (id, month) NOT IN (
    SELECT id, MAX(month)
    FROM Employee
    GROUP BY id
)
ORDER BY id, month DESC;
```

> Both queries return the same result on the example dataset. Solution 1 is the more
> direct idiom — the exclusion falls out of the same `PARTITION BY id` used for the sum;
> Solution 2 needs a second pass over `Employee` to find each employee's latest month.

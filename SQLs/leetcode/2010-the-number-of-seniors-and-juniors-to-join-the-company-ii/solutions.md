# 2010. The Number of Seniors and Juniors to Join the Company II - Solutions

## Solution 1: Remaining budget per row

Track the running *budget remaining* directly: `remaining_budget = 70000 - running_total`. A senior row is affordable whenever `remaining_budget >= 0`. Because `remaining_budget` decreases monotonically as salary rank increases, `MIN(remaining_budget)` among the affordable senior rows is exactly the leftover budget after hiring the maximum number of seniors — no further arithmetic needed. That leftover is isolated in its own `remaining` CTE and reused as the starting budget for juniors (falling back to the full $70000 via `COALESCE` when no senior is affordable).

The `remaining` CTE must filter with `remaining_budget >= 0`, not `> 0` — if the cheapest-affordable seniors' running total lands exactly on $70000, that row's `remaining_budget` is `0` and needs to stay in the `MIN()`, or the leftover budget is computed from an earlier (larger, incorrect) row and juniors get hired against a phantom budget.

#### MySQL

```sql
WITH senior AS (
    SELECT
        employee_id,
        experience,
        salary,
        70000 - SUM(salary) OVER (ORDER BY salary, employee_id) AS remaining_budget
    FROM Candidates
    WHERE experience = 'Senior'
), remaining AS (
    SELECT COALESCE(MIN(remaining_budget), 70000) AS budget
    FROM senior
    WHERE remaining_budget >= 0
), junior AS (
    SELECT
        employee_id,
        experience,
        salary,
        (SELECT budget FROM remaining) - SUM(salary) OVER (ORDER BY salary, employee_id) AS remaining_budget
    FROM Candidates
    WHERE experience = 'Junior'
)
SELECT employee_id FROM senior WHERE remaining_budget >= 0
UNION
SELECT employee_id FROM junior WHERE remaining_budget >= 0;
```

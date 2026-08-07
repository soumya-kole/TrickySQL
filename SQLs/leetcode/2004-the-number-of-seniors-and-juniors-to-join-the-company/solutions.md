# 2004. The Number of Seniors and Juniors to Join the Company - Solutions

## Solution 1: Remaining budget per row

Track the running *budget remaining* directly: `rs = 70000 - running_total`. A row is affordable whenever `rs >= 0`. Because `rs` decreases monotonically as salary rank increases, `MIN(rs)` among the affordable senior rows is exactly the leftover budget after hiring the maximum number of seniors — no further arithmetic needed. That leftover is isolated in its own `remaining` CTE and reused as the starting budget for juniors (falling back to the full $70000 via `COALESCE` when no senior is affordable).

#### MySQL

```sql
WITH s AS (
    SELECT
        employee_id,
        experience,
        salary,
        70000 - SUM(salary) OVER (ORDER BY salary, employee_id) AS rs
    FROM Candidates
    WHERE experience = 'Senior'
),
remaining AS (
    SELECT COALESCE((SELECT MIN(rs) FROM s WHERE rs >= 0), 70000) AS budget
),
j AS (
    SELECT
        employee_id,
        experience,
        salary,
        (SELECT budget FROM remaining) - SUM(salary) OVER (ORDER BY salary, employee_id) AS rs
    FROM Candidates
    WHERE experience = 'Junior'
)
SELECT experience, COUNT(*) AS accepted_candidates FROM s WHERE rs >= 0 GROUP BY experience
UNION ALL
SELECT experience, COUNT(*) AS accepted_candidates FROM j WHERE rs >= 0 GROUP BY experience;
```

## Solution 2: Running total with window functions

Order each experience group by salary (cheapest first) and compute a running total with `SUM() OVER (ORDER BY ...)`. The greedy rule "hire as many as possible within budget" is equivalent to counting how many of the smallest salaries fit under the running budget. Seniors are evaluated against the full $70000 budget first; juniors are then evaluated against whatever budget is left after the seniors are hired.

#### MySQL

```sql
WITH senior_cte AS (
    SELECT
        employee_id,
        SUM(salary) OVER (ORDER BY salary, employee_id) AS running_total
    FROM Candidates
    WHERE experience = 'Senior'
),
senior_spent AS (
    SELECT COALESCE(MAX(running_total), 0) AS spent
    FROM senior_cte
    WHERE running_total <= 70000
),
junior_cte AS (
    SELECT
        employee_id,
        (SELECT spent FROM senior_spent) + SUM(salary) OVER (ORDER BY salary, employee_id) AS running_total
    FROM Candidates
    WHERE experience = 'Junior'
)
SELECT 'Senior' AS experience, COUNT(*) AS accepted_candidates
FROM senior_cte
WHERE running_total <= 70000
UNION ALL
SELECT 'Junior' AS experience, COUNT(*) AS accepted_candidates
FROM junior_cte
WHERE running_total <= 70000;
```

# 2394. Employees With Deductions - Solutions

## Solution 1: Round each session up to the minute, sum, then compare against the requirement

Each session's worked time must be rounded *up* to the nearest minute before summing — `TIMESTAMPDIFF(SECOND, in_time, out_time)` gives the exact duration in seconds, and `CEILING(... / 60)` rounds that up to whole minutes (matching the example: 3 minutes 59 seconds still becomes 4 minutes, and 58 seconds becomes 1 minute). Summing those per-session minutes per employee and dividing by 60 gives total hours worked.

An employee with no logs at all (like employee 3) never appears in that aggregate, so a `LEFT JOIN` from `Employees` is needed to keep them in the result, with `COALESCE(..., 0)` treating "no sessions" as zero hours worked.

#### MySQL

```sql
WITH worked AS (
    SELECT
        employee_id,
        SUM(CEILING(TIMESTAMPDIFF(SECOND, in_time, out_time) / 60)) / 60 AS hours_worked
    FROM Logs
    GROUP BY employee_id
)
SELECT e.employee_id
FROM Employees e
LEFT JOIN worked w ON w.employee_id = e.employee_id
WHERE COALESCE(w.hours_worked, 0) < e.needed_hours;
```
If Logs has multiple months data and if employee should be included if during any month there was a shortfall, then we need following query:
``` sql
WITH worked AS (
    SELECT
        employee_id,
        DATE_FORMAT(in_time, '%Y-%m') AS work_month,
       sum(CEILING(TIMESTAMPDIFF(SECOND, in_time, out_time)/60)/60)  AS hours_worked
    FROM Logs
    GROUP BY employee_id, work_month
),
months AS (
    SELECT DISTINCT
        DATE_FORMAT(in_time, '%Y-%m') AS work_month
    FROM Logs
),
monthwise AS (
    SELECT
        m.work_month,
        e.employee_id,
        e.needed_hours
    FROM months m
    CROSS JOIN Employees e
)
SELECT DISTINCT mw.employee_id
FROM monthwise mw
LEFT JOIN worked w
    ON w.employee_id = mw.employee_id
    AND w.work_month = mw.work_month
WHERE COALESCE(w.hours_worked, 0) < mw.needed_hours;
```

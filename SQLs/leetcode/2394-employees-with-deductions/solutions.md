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

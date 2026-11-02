# 1270. All People Report to the Given Manager - Solutions

## Solution 1: Two self-joins walk the chain up to the head

The reporting chain is bounded at three hops, so there's no need for a recursive CTE — two self-joins on `Employees` walk from boos to first level and from first level to second level employees.



#### MySQL
```sql
SELECT e3.employee_id
FROM Employees e1 -- Boss
JOIN Employees e2 ON e1.employee_id = e2.manager_id -- First Level
JOIN Employees e3 ON e2.employee_id = e3.manager_id -- Second Level
WHERE 
e3.employee_id != 1 AND -- Exclude Boss
e1.manager_id = 1; -- Identify boss
```
In case of unknown hops, a recursive CTE would be required:

``` sql
WITH RECURSIVE report AS (
    SELECT
        employee_id
    FROM Employees
    WHERE manager_id = 1
      AND employee_id != 1
    UNION ALL
    SELECT
        e.employee_id
    FROM Employees e
    JOIN report r
        ON e.manager_id = r.employee_id
)
SELECT *
FROM report;
```

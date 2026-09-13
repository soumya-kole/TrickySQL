# 1270. All People Report to the Given Manager - Solutions

## Solution 1: Two self-joins walk the chain up to the head

The reporting chain is bounded at three hops, so there's no need for a recursive CTE — two self-joins on `Employees` walk from an employee to their manager, then to that manager's manager, which is enough to cover every case in the constraint.

The head of the company (`employee_id = 1`) is its own manager, so a short chain like `2 -> 1` still resolves correctly: joining past the head just lands back on the head each time (`e2` and `e3` both become the Boss row), and `e3.manager_id = 1` still holds. Excluding `e1.employee_id = 1` keeps the head itself out of its own result.

#### MySQL

```sql
SELECT e1.employee_id
FROM Employees e1
JOIN Employees e2 ON e1.manager_id = e2.employee_id
JOIN Employees e3 ON e2.manager_id = e3.employee_id
WHERE e1.employee_id != 1 AND e3.manager_id = 1;
```

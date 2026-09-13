# 1440. Evaluate Boolean Expression - Solutions

## Solution 1: Double equi-join + `CASE`

`Expressions` stores operand *names*, not values, so each row needs two lookups into `Variables` — one for `left_operand`, one for `right_operand`. Joining `Variables` twice (aliased `v1`, `v2`) resolves both values on the same row, and a `CASE` then matches the row's `operator` against the appropriate comparison of `v1.value` and `v2.value`.

#### MySQL

```sql
SELECT
    e.left_operand,
    e.operator,
    e.right_operand,
    CASE
        WHEN e.operator = '=' AND v1.value = v2.value THEN 'true'
        WHEN e.operator = '>' AND v1.value > v2.value THEN 'true'
        WHEN e.operator = '<' AND v1.value < v2.value THEN 'true'
        ELSE 'false'
    END AS value
FROM Expressions e
JOIN Variables v1 ON v1.name = e.left_operand
JOIN Variables v2 ON v2.name = e.right_operand;
```

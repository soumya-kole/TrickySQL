# Explode Implementation - Solutions

## Solution 1: Recursive CTE

Peel off the first comma-separated token with `SUBSTRING_INDEX(csv_column, ',', 1)`, then
recurse on whatever remains after that token and its trailing comma. Recursion stops once
`remaining_values` is empty, i.e. the last token has been emitted.

#### MySQL

```sql
WITH RECURSIVE cte AS (
    SELECT
        id,
        SUBSTRING_INDEX(csv_column, ',', 1) AS value,
        SUBSTRING(csv_column, LENGTH(SUBSTRING_INDEX(csv_column, ',', 1)) + 2) AS remaining_values
    FROM explode_table
    UNION ALL
    SELECT
        id,
        SUBSTRING_INDEX(remaining_values, ',', 1) AS value,
        SUBSTRING(remaining_values, LENGTH(SUBSTRING_INDEX(remaining_values, ',', 1)) + 2) AS remaining_values
    FROM cte
    WHERE remaining_values <> ''
)
SELECT id, value
FROM cte
ORDER BY id;
```

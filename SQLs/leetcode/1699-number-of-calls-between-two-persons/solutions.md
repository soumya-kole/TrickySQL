# 1699. Number of Calls Between Two Persons - Solutions

## Solution 1: Normalise the pair, then group

A call from 1 to 2 and a call from 2 to 1 belong to the same pair, so the direction
has to be thrown away before grouping. `LEAST()` / `GREATEST()` map every row onto the
canonical ordering `person1 < person2`; grouping on those two derived columns then
collapses both directions into one row per pair.

#### MySQL

```sql
SELECT
    LEAST(from_id, to_id)    AS person1,
    GREATEST(from_id, to_id) AS person2,
    COUNT(*)                 AS call_count,
    SUM(duration)            AS total_duration
FROM Calls
GROUP BY person1, person2;
```

## Solution 2: `CASE` instead of `LEAST` / `GREATEST`

Same idea, spelled out with a conditional. Useful on engines that lack
`LEAST`/`GREATEST` (or when you need to carry along other columns from the "smaller"
side, where a plain min/max would not work). `CASE` is standard SQL, so this runs
unchanged on PostgreSQL, SQL Server, Oracle, SQLite, etc.

#### MySQL

```sql
SELECT
    CASE WHEN from_id < to_id THEN from_id ELSE to_id END AS person1,
    CASE WHEN from_id < to_id THEN to_id ELSE from_id END AS person2,
    COUNT(*)      AS call_count,
    SUM(duration) AS total_duration
FROM Calls
GROUP BY person1, person2;
```

Note that the table has no primary key and contains exact duplicate rows
(`3, 4, 200` appears twice). Both must be counted, so `COUNT(*)` is correct here and
`COUNT(DISTINCT ...)` would be wrong.

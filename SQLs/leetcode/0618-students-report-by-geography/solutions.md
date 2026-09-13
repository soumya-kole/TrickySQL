# 618. Students Report By Geography - Solutions

## Solution 1: Row Number + Pivot

Assign each name a per-continent rank with `ROW_NUMBER()` ordered alphabetically, so the 1st-ranked American, 1st-ranked Asian, and 1st-ranked European all get `rk = 1`, the 2nd-ranked students from each continent get `rk = 2`, and so on. Grouping by `rk` and pivoting `continent` into columns with `MAX(CASE WHEN ... END)` then places same-rank students from different continents onto the same output row, letting `MAX` collapse each group's `NULL`s down to the one non-`NULL` value that matches that column's continent (or `NULL` if no student from that continent shares that rank).

#### MySQL

```sql
WITH ranked AS (
    SELECT
        name,
        continent,
        ROW_NUMBER() OVER (PARTITION BY continent ORDER BY name) AS rk
    FROM Student
)
SELECT
    MAX(CASE WHEN continent = 'America' THEN name END) AS America,
    MAX(CASE WHEN continent = 'Asia' THEN name END)    AS Asia,
    MAX(CASE WHEN continent = 'Europe' THEN name END)  AS Europe
FROM ranked
GROUP BY rk
ORDER BY rk;
```

**Follow-up:** this already works without assuming America has the most students. `GROUP BY rk` groups rows by rank alone, independent of continent, so whichever continent happens to have the highest count simply produces the largest `rk` values and the most output rows — the other columns fall back to `NULL` via `MAX(CASE ...)` once their continent runs out of ranked names. Verify against `## Setup2` (Asia has the most students there) — the query still returns the correct pivoted, alphabetically-sorted report.

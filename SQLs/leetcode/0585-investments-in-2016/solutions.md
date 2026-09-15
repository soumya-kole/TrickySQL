# 585. Investments in 2016 - Solutions

## Solution 1: Window Functions

Count how many rows share each `tiv_2015` and how many rows share each `(lat, lon)` pair using `COUNT(*) OVER (PARTITION BY ...)`. A policy qualifies when its `tiv_2015` count is greater than 1 (shared with someone else) and its `(lat, lon)` count equals 1 (unique location). Summing `tiv_2016` over the qualifying rows and rounding gives the answer in a single pass.

#### MySQL

```sql
WITH cte AS (
    SELECT
        tiv_2016,
        COUNT(*) OVER (PARTITION BY tiv_2015) AS tiv_2015_cnt,
        COUNT(*) OVER (PARTITION BY lat, lon) AS location_cnt
    FROM Insurance
)
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM cte
WHERE tiv_2015_cnt > 1 AND location_cnt = 1;
```

## Solution 2: Grouped Subqueries

Build the same two conditions as separate lookups: one subquery groups by `tiv_2015` and keeps values that appear more than once, the other groups by `(lat, lon)` and keeps pairs that appear exactly once. Filtering `Insurance` against both lookups isolates the qualifying policies before summing and rounding `tiv_2016`.

#### MySQL

```sql
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance
WHERE tiv_2015 IN (
    SELECT tiv_2015
    FROM Insurance
    GROUP BY tiv_2015
    HAVING COUNT(*) > 1
)
AND (lat, lon) IN (
    SELECT lat, lon
    FROM Insurance
    GROUP BY lat, lon
    HAVING COUNT(*) = 1
);
```

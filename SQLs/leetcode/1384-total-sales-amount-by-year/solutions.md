# 1384. Total Sales Amount by Year - Solutions

## Solution 1

A recursive CTE builds the set of calendar years actually spanned by
`Sales` (`YEAR(MIN(period_start))` through `YEAR(MAX(period_end))`)
instead of hardcoding `2018`–`2020`, and `DAYOFYEAR(CONCAT(report_year,
'-12-31'))` derives each year's length (365 or 366) instead of hardcoding
leap years. Joining `Sales` to `year_lengths` on `report_year BETWEEN
YEAR(period_start) AND YEAR(period_end)` always finds at least one match,
so a plain `JOIN` is enough — no row can produce a `NULL`, which is also
why the four `CASE` branches (start/end year vs. `report_year`) are
exhaustive with no `ELSE` needed. Each branch computes the number of days
of the sale that fall in that report year, multiplied by
`average_daily_sales`.

#### MySQL

```sql
WITH RECURSIVE years AS (
    SELECT YEAR(MIN(period_start)) AS report_year
    FROM Sales
    UNION ALL
    SELECT report_year + 1
    FROM years
    WHERE report_year < (SELECT YEAR(MAX(period_end)) FROM Sales)
),
year_lengths AS (
    SELECT report_year, DAYOFYEAR(CONCAT(report_year, '-12-31')) AS days_in_year
    FROM years
)
SELECT
    s.product_id,
    p.product_name,
    y.report_year,
    (CASE
        WHEN YEAR(s.period_start) = y.report_year AND YEAR(s.period_end) = y.report_year
            THEN DATEDIFF(s.period_end, s.period_start) + 1
        WHEN YEAR(s.period_start) = y.report_year AND YEAR(s.period_end) > y.report_year
            THEN y.days_in_year - DAYOFYEAR(s.period_start) + 1
        WHEN YEAR(s.period_start) < y.report_year AND YEAR(s.period_end) > y.report_year
            THEN y.days_in_year
        WHEN YEAR(s.period_start) < y.report_year AND YEAR(s.period_end) = y.report_year
            THEN DAYOFYEAR(s.period_end)
    END) * s.average_daily_sales AS total_amount
FROM Sales s
JOIN year_lengths y ON y.report_year BETWEEN YEAR(s.period_start) AND YEAR(s.period_end)
JOIN Product p ON p.product_id = s.product_id
ORDER BY s.product_id, y.report_year;
```

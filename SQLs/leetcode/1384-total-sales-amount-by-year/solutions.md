# 1384. Total Sales Amount by Year - Solutions

## Solution 1

A recursive CTE builds the set of calendar years actually spanned by
`Sales` (`YEAR(MIN(period_start))` through `YEAR(MAX(period_end))`)
instead of hardcoding `2018`–`2020`, and pairs each `report_year` with its
`year_start`/`year_end` bounds (`report_year-01-01` / `report_year-12-31`).
Joining `Sales` to `year_bounds` on `report_year BETWEEN
YEAR(period_start) AND YEAR(period_end)` always finds at least one match,
so a plain `JOIN` is enough — no row can produce a `NULL`. The number of
days of a sale that fall within a given report year is then just the
overlap between `[period_start, period_end]` and `[year_start, year_end]`:
the later of the two start dates through the earlier of the two end
dates, each picked with a `CASE` rather than `GREATEST`/`LEAST`.

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
year_bounds AS (
    SELECT
        report_year,
        CONCAT(report_year, '-01-01') AS year_start,
        CONCAT(report_year, '-12-31') AS year_end
    FROM years
)
SELECT
    s.product_id,
    p.product_name,
    y.report_year,
    (DATEDIFF(
        CASE WHEN s.period_end < y.year_end THEN s.period_end ELSE y.year_end END,
        CASE WHEN s.period_start > y.year_start THEN s.period_start ELSE y.year_start END
    ) + 1) * s.average_daily_sales AS total_amount
FROM Sales s
JOIN year_bounds y ON y.report_year BETWEEN YEAR(s.period_start) AND YEAR(s.period_end)
JOIN Product p ON p.product_id = s.product_id
ORDER BY s.product_id, y.report_year;
```

## Solution 2

Same recursive CTE to generate the report years, but instead of computing
the overlap directly, `year_lengths` precomputes each year's length in
days (`DAYOFYEAR(CONCAT(report_year, '-12-31'))`, so `366` in a leap
year), and a 4-branch `CASE` handles each way a sale's start/end year can
relate to `report_year`: fully inside it, starting in it but ending
later, starting earlier but ending in it, or spanning across it entirely.

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

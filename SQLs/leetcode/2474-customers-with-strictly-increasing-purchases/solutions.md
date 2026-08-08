# 2474. Customers With Strictly Increasing Purchases - Solutions

## Solution 1

Instead of filling in every year between a customer's first and last order, this
compares each pair of *consecutive actual order-years* directly with `LAG()`. A
missing year always resets that year's total to 0, and since any real order-year
total is positive, a gap always breaks strict increase — so requiring the year-gap
between consecutive order-years to be exactly `1` (no gaps at all) is equivalent to
requiring the full, 0-filled sequence to be strictly increasing.

A customer with only a single order-year has no row to compare (`LAG()` yields
`NULL`), so it's handled separately: with just one year, there's nothing to
violate, so it's trivially "strictly increasing" and included unconditionally.

Validate against [Setup2](setup.md#setup2), which adds a two-year strictly
increasing customer and a single-order-year customer — both must appear in the
result.

#### MySQL

```sql
WITH yearly AS (
    SELECT
        customer_id,
        YEAR(order_date) AS yr,
        SUM(price) AS total_price
    FROM Orders
    GROUP BY customer_id, YEAR(order_date)
),
diffs AS (
    SELECT
        customer_id,
        yr - LAG(yr) OVER (PARTITION BY customer_id ORDER BY yr) AS yr_gap,
        total_price - LAG(total_price) OVER (PARTITION BY customer_id ORDER BY yr) AS price_diff
    FROM yearly
),
multi_year AS (
    SELECT customer_id
    FROM diffs
    WHERE yr_gap IS NOT NULL
    GROUP BY customer_id
    HAVING MAX(yr_gap) = 1 AND MIN(price_diff) > 0
),
single_year AS (
    SELECT customer_id
    FROM yearly
    GROUP BY customer_id
    HAVING COUNT(*) = 1
)
SELECT customer_id FROM multi_year
UNION
SELECT customer_id FROM single_year;
```

## Solution 2

#### MySQL

```sql
WITH RECURSIVE customer_range AS (
    SELECT
        customer_id,
        YEAR(MIN(order_date)) AS start_year,
        YEAR(MAX(order_date)) AS end_year
    FROM Orders
    GROUP BY customer_id
),
years AS (
    SELECT customer_id, start_year AS yr, end_year
    FROM customer_range

    UNION ALL

    SELECT customer_id, yr + 1, end_year
    FROM years
    WHERE yr < end_year
),
yearly_totals AS (
    SELECT
        customer_id,
        YEAR(order_date) AS yr,
        SUM(price) AS total
    FROM Orders
    GROUP BY customer_id, YEAR(order_date)
),
filled AS (
    SELECT
        y.customer_id,
        y.yr,
        COALESCE(t.total, 0) AS total
    FROM years y
    LEFT JOIN yearly_totals t
        ON t.customer_id = y.customer_id AND t.yr = y.yr
),
flagged AS (
    SELECT
        customer_id,
        total,
        LAG(total) OVER (PARTITION BY customer_id ORDER BY yr) AS prev_total
    FROM filled
)
SELECT customer_id
FROM flagged
GROUP BY customer_id
HAVING SUM(CASE WHEN prev_total IS NOT NULL AND total <= prev_total THEN 1 ELSE 0 END) = 0;
```

# 1445. Apples & Oranges - Solutions

## Solution 1

Each `sale_date` has exactly one `apples` row and one `oranges` row (the
table's primary key is `(sale_date, fruit)`), so `MAX(CASE WHEN fruit = ...
THEN sold_num ELSE 0 END)` per fruit just picks out that row's `sold_num` —
the `MAX` isn't aggregating multiple values, it's a trick for pivoting the two
fruit rows into two columns within the same `GROUP BY sale_date`. Subtracting
the two pivoted columns then gives the diff directly.

#### MySQL

```sql
SELECT
    sale_date,
    MAX(CASE WHEN fruit = 'apples' THEN sold_num ELSE 0 END) -
    MAX(CASE WHEN fruit = 'oranges' THEN sold_num ELSE 0 END) AS diff
FROM Sales
GROUP BY sale_date;
```

## Solution 2

`SUM(CASE WHEN fruit = 'apples' THEN sold_num ELSE -sold_num END)` turns each
row's `sold_num` into a signed contribution before it's ever aggregated:
apples rows keep their positive value, oranges rows get negated. Summing that
per `sale_date` gives apples_total - oranges_total directly, in one pass,
rather than computing the two totals separately (as in Solution 1) and
subtracting them afterward.

#### MySQL

```sql
SELECT
    sale_date,
    SUM(CASE
        WHEN fruit = 'apples' THEN sold_num
        ELSE -sold_num
    END) AS diff
FROM Sales
GROUP BY sale_date
ORDER BY sale_date;
```

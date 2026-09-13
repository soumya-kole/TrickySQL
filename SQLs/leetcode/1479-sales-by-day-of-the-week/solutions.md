# 1479. Sales by Day of the Week - Solutions

## Solution 1

`Items` drives the query on the left so that a category with no orders at
all — `T-Shirt` in the sample data — still produces a row of all zeros
instead of disappearing, which a plain inner join against `Orders` would
do. `DAYOFWEEK(order_date)` returns `1` for Sunday through `7` for
Saturday, so each weekday column is a `CASE` that keeps `quantity` when
the order falls on that weekday and `0` otherwise, summed per category.
Rows from `Orders` that don't match any weekday's `CASE` just contribute
`0` to that column, and the unmatched (`NULL`) `quantity` for categories
with no orders at all also sums to `0` via `SUM`'s handling of `NULL`
input.

#### MySQL

```sql
SELECT
    item_category AS category,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 2 THEN quantity ELSE 0 END) AS Monday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 3 THEN quantity ELSE 0 END) AS Tuesday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 4 THEN quantity ELSE 0 END) AS Wednesday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 5 THEN quantity ELSE 0 END) AS Thursday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 6 THEN quantity ELSE 0 END) AS Friday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 7 THEN quantity ELSE 0 END) AS Saturday,
    SUM(CASE WHEN DAYOFWEEK(order_date) = 1 THEN quantity ELSE 0 END) AS Sunday
FROM
    Items AS i
    LEFT JOIN Orders AS o ON o.item_id = i.item_id
GROUP BY category
ORDER BY category;
```

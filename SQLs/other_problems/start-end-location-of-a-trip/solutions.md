# Start and End Location of a Trip - Solutions

## Solution 1: Anti-join via `NOT IN`, per customer

For each customer, the overall start is the `start_loc` that never shows up as one of that customer's `end_loc` values, and the overall end is the `end_loc` that never shows up as one of that customer's `start_loc` values. A correlated `NOT IN` subquery finds each, and `MAX` collapses the per-row `CASE` result down to one value per customer.

#### MySQL

```sql
SELECT
    customer,
    MAX(CASE
        WHEN start_loc NOT IN (
            SELECT end_loc FROM travel_data t2 WHERE t2.customer = t1.customer
        ) THEN start_loc
    END) AS start_loc,
    MAX(CASE
        WHEN end_loc NOT IN (
            SELECT start_loc FROM travel_data t2 WHERE t2.customer = t1.customer
        ) THEN end_loc
    END) AS end_loc
FROM travel_data t1
GROUP BY customer
ORDER BY customer;
```

# 2362. Generate the Invoice - Solutions

## Solution 1

#### MySQL

```sql
WITH
    p AS (
        SELECT *
        FROM Purchases
        JOIN Products USING (product_id)
    ),
    t AS (
        SELECT invoice_id, SUM(price * quantity) AS amount
        FROM p
        GROUP BY invoice_id
        ORDER BY amount DESC, invoice_id
        LIMIT 1
    )
SELECT product_id, quantity, (quantity * price) AS price
FROM p
JOIN t USING (invoice_id);
```

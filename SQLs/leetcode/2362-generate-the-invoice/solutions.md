# 2362. Generate the Invoice - Solutions

## Solution 1

#### MySQL

```sql
WITH cte AS (
    SELECT
        pu.invoice_id,
        pu.product_id,
        pu.quantity,
        pu.quantity * po.price AS price,
        SUM(pu.quantity * po.price) OVER (PARTITION BY pu.invoice_id) AS total_price
    FROM Purchases pu
    JOIN Products po ON pu.product_id = po.product_id
)
SELECT product_id, quantity, price
FROM cte
WHERE invoice_id = (SELECT invoice_id FROM cte ORDER BY total_price DESC, invoice_id ASC LIMIT 1);
```

## Solution 2

#### MySQL

```sql
WITH cte AS (
    SELECT
        pu.invoice_id,
        pu.product_id,
        pu.quantity,
        pu.quantity * po.price AS price
    FROM Purchases pu
    JOIN Products po ON pu.product_id = po.product_id
),
cte2 AS (
    SELECT invoice_id, SUM(price) AS price
    FROM cte
    GROUP BY invoice_id
)
SELECT product_id, quantity, price
FROM cte
WHERE invoice_id = (
    SELECT min(invoice_id)
    FROM cte2
    WHERE price = (SELECT max(price) FROM cte2)
);
```

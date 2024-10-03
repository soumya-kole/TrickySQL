## Objective
Let’s say we have two tables, transactions and products. Hypothetically the transactions table consists of over a billion rows of purchases bought by users.
We are trying to find paired products that are often purchased together in same transaction, such as wine and bottle openers, chips and beer, etc..
Write a query to find the top five paired products and their names order by pair count and total qty.
Notes: For the purposes of satisfying the test case, p1 should be the item that comes first in the alphabet. 

## Data preparation

```sql
CREATE TABLE wired-coda-437404-m5.query_practice.transactions (
    transaction_id INT64,
    user_id INT64,
    created_at DATETIME,
    product_id INT64,
    quantity INT64
);

CREATE TABLE wired-coda-437404-m5.query_practice.products (
    id INT64,
    name STRING,
    price FLOAT64
);

INSERT INTO wired-coda-437404-m5.query_practice.products (id, name, price) VALUES
    (1, 'Wine', 15.00),
    (2, 'Bottle Opener', 5.00),
    (3, 'Chips', 2.50),
    (4, 'Beer', 8.00),
    (5, 'Soda', 3.00);

INSERT INTO wired-coda-437404-m5.query_practice.transactions (transaction_id, user_id, created_at, product_id, quantity) VALUES
    (1, 101, '2024-10-01 12:00:00', 1, 1), -- Wine
    (1, 101, '2024-10-01 12:00:00', 2, 1), -- Bottle Opener
    (1, 101, '2024-10-01 12:00:00', 4, 1), -- Bottle Opener
    (6, 101, '2024-10-01 13:00:00', 1, 1), -- Wine
    (6, 101, '2024-10-01 13:00:00', 2, 1), -- Bottle Opener
    (2, 102, '2024-10-01 12:30:00', 3, 2), -- Chips
    (2, 102, '2024-10-01 12:30:00', 4, 1), -- Beer
    (3, 103, '2024-10-01 13:00:00', 1, 1), -- Wine
    (3, 103, '2024-10-01 13:00:00', 4, 1), -- Beer
    (4, 104, '2024-10-01 14:00:00', 3, 3), -- Chips
    (4, 104, '2024-10-01 14:00:00', 2, 1), -- Bottle Opener
    (5, 105, '2024-10-01 14:30:00', 5, 2), -- Soda
    (5, 105, '2024-10-01 14:30:00', 1, 1); -- Wine

```

## Solution

```sql
with cte as (
select 
    t1.product_id as pid1, t2.product_id as pid2, count(*) as pair_cnt, sum(t1.quantity) as total_qty
from 
  `wired-coda-437404-m5.query_practice.transactions` as t1
  join 
  `wired-coda-437404-m5.query_practice.transactions`  as t2
on 
  t1.transaction_id = t2.transaction_id
  and t1.product_id < t2.product_id
group by 1, 2
order by 3 desc,4 desc
limit 3
)
select 
  least(p1.name, p2.name) as p1,
  greatest(p1.name, p2.name) as p2,
  c.pair_cnt,
  c.total_qty
from cte c
  join wired-coda-437404-m5.query_practice.products p1
  on c.pid1 = p1.id
  join wired-coda-437404-m5.query_practice.products p2
  on c.pid2 = p2.id
order by 3 desc, 4 desc, 1, 2
```

## Output
![img](../Images/paired_products.png)

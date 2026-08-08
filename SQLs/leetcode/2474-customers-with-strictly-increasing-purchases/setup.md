# 2474. Customers With Strictly Increasing Purchases - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    price       INT
);

INSERT INTO Orders (order_id, customer_id, order_date, price) VALUES
(1, 1, '2019-07-01', 1100),
(2, 1, '2019-11-01', 1200),
(3, 1, '2020-05-26', 3000),
(4, 1, '2021-08-31', 3100),
(5, 1, '2022-12-07', 4700),
(6, 2, '2015-01-01', 700),
(7, 2, '2017-11-07', 1000),
(8, 3, '2017-01-01', 900),
(9, 3, '2018-11-07', 900);
```

Load this dataset:

```bash
make setup 2474-customers-with-strictly-increasing-purchases
```

## Setup2

Adds two customers that stress the "compare consecutive actual order-years"
approach:

- **Customer 4** — orders in exactly two consecutive years, strictly increasing
  (2020: 100 → 2021: 200). This is simply the minimum valid input for "strictly
  increasing yearly" — two years, one comparison — and must be included; it is not
  a corner case. A query that additionally filters on the number of comparisons
  (e.g. requiring more than one) wrongly excludes it.
- **Customer 5** — a single order, in a single year (2020: 500). With only one year
  to consider there's nothing to violate, so this customer is trivially "strictly
  increasing" and must be included. A solution built purely from
  `LAG() OVER (...)` row-to-row comparisons naturally produces zero comparable rows
  for a single-year customer and silently drops them unless handled separately.

Expected `customer_id` output: `1, 4, 5`.

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    price       INT
);

INSERT INTO Orders (order_id, customer_id, order_date, price) VALUES
(1, 1, '2019-07-01', 1100),
(2, 1, '2019-11-01', 1200),
(3, 1, '2020-05-26', 3000),
(4, 1, '2021-08-31', 3100),
(5, 1, '2022-12-07', 4700),
(6, 2, '2015-01-01', 700),
(7, 2, '2017-11-07', 1000),
(8, 3, '2017-01-01', 900),
(9, 3, '2018-11-07', 900),
(10, 4, '2020-01-01', 100),
(11, 4, '2021-01-01', 200),
(12, 5, '2020-01-01', 500);
```

Load this dataset:

```bash
make setup 2474-customers-with-strictly-increasing-purchases 2
```

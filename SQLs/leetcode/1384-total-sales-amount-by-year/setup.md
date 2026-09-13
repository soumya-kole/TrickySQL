# 1384. Total Sales Amount by Year - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(50)
);

CREATE TABLE Sales (
    product_id          INT PRIMARY KEY,
    period_start         DATE,
    period_end           DATE,
    average_daily_sales   INT
);

INSERT INTO Product (product_id, product_name) VALUES
(1, 'LC Phone'),
(2, 'LC T-Shirt'),
(3, 'LC Keychain');

INSERT INTO Sales (product_id, period_start, period_end, average_daily_sales) VALUES
(1, '2019-01-25', '2019-02-28', 100),
(2, '2018-12-01', '2020-01-01', 10),
(3, '2019-12-01', '2020-01-31', 1);
```

Load this dataset:

```bash
make setup 1384-total-sales-amount-by-year
```

# 1479. Sales by Day of the Week - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Items;

CREATE TABLE Items (
    item_id       VARCHAR(10) PRIMARY KEY,
    item_name     VARCHAR(50),
    item_category VARCHAR(50)
);

CREATE TABLE Orders (
    order_id    INT,
    customer_id INT,
    order_date  DATE,
    item_id     VARCHAR(10),
    quantity    INT,
    PRIMARY KEY (order_id, item_id)
);

INSERT INTO Items (item_id, item_name, item_category) VALUES
('1', 'LC Alg. Book', 'Book'),
('2', 'LC DB. Book', 'Book'),
('3', 'LC SmarthPhone', 'Phone'),
('4', 'LC Phone 2020', 'Phone'),
('5', 'LC SmartGlass', 'Glasses'),
('6', 'LC T-Shirt XL', 'T-Shirt');

INSERT INTO Orders (order_id, customer_id, order_date, item_id, quantity) VALUES
(1, 1, '2020-06-01', '1', 10),
(2, 1, '2020-06-08', '2', 10),
(3, 2, '2020-06-02', '1', 5),
(4, 3, '2020-06-03', '3', 5),
(5, 4, '2020-06-04', '4', 1),
(6, 4, '2020-06-05', '5', 5),
(7, 5, '2020-06-05', '1', 10),
(8, 5, '2020-06-14', '4', 5),
(9, 5, '2020-06-21', '3', 5);
```

Load this dataset:

```bash
make setup 1479-sales-by-day-of-the-week
```

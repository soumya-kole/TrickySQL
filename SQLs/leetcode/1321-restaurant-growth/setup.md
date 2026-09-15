# 1321. Restaurant Growth - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
    customer_id INT,
    name        VARCHAR(30),
    visited_on  DATE,
    amount      INT,
    PRIMARY KEY (customer_id, visited_on)
);

INSERT INTO Customer (customer_id, name, visited_on, amount) VALUES
(1, 'Jhon',    '2019-01-01', 100),
(2, 'Daniel',  '2019-01-02', 110),
(3, 'Jade',    '2019-01-03', 120),
(4, 'Khaled',  '2019-01-04', 130),
(5, 'Winston', '2019-01-05', 110),
(6, 'Elvis',   '2019-01-06', 140),
(7, 'Anna',    '2019-01-07', 150),
(8, 'Maria',   '2019-01-08', 80),
(9, 'Jaze',    '2019-01-09', 110),
(1, 'Jhon',    '2019-01-10', 130),
(3, 'Jade',    '2019-01-10', 150);
```

Load this dataset:

```bash
make setup 1321-restaurant-growth
```

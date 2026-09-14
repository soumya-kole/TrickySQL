# Paired Products (Frequently Bought Together) - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id    INT PRIMARY KEY,
    name  VARCHAR(50),
    price DECIMAL(10, 2)
);

CREATE TABLE transactions (
    transaction_id INT,
    user_id        INT,
    created_at     DATETIME,
    product_id     INT,
    quantity       INT
);

INSERT INTO products (id, name, price) VALUES
(1, 'Wine', 15.00),
(2, 'Bottle Opener', 5.00),
(3, 'Chips', 2.50),
(4, 'Beer', 8.00),
(5, 'Soda', 3.00);

INSERT INTO transactions (transaction_id, user_id, created_at, product_id, quantity) VALUES
(1, 101, '2024-10-01 12:00:00', 1, 1),
(1, 101, '2024-10-01 12:00:00', 2, 1),
(1, 101, '2024-10-01 12:00:00', 4, 1),
(6, 101, '2024-10-01 13:00:00', 1, 1),
(6, 101, '2024-10-01 13:00:00', 2, 1),
(2, 102, '2024-10-01 12:30:00', 3, 2),
(2, 102, '2024-10-01 12:30:00', 4, 1),
(3, 103, '2024-10-01 13:00:00', 1, 1),
(3, 103, '2024-10-01 13:00:00', 4, 1),
(4, 104, '2024-10-01 14:00:00', 3, 3),
(4, 104, '2024-10-01 14:00:00', 2, 1),
(5, 105, '2024-10-01 14:30:00', 5, 2),
(5, 105, '2024-10-01 14:30:00', 1, 1);
```

Load this dataset:

```bash
make setup paired-products-frequently-bought-together
```

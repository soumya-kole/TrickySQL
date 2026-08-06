# 2362. Generate the Invoice - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Purchases;
DROP TABLE IF EXISTS Products;

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    price      INT
);

CREATE TABLE Purchases (
    invoice_id INT,
    product_id INT,
    quantity   INT,
    PRIMARY KEY (invoice_id, product_id)
);

INSERT INTO Products (product_id, price) VALUES
(1, 100),
(2, 200);

INSERT INTO Purchases (invoice_id, product_id, quantity) VALUES
(1, 1, 2),
(3, 2, 1),
(2, 2, 3),
(2, 1, 4),
(4, 1, 10);
```

Load this dataset:

```bash
make setup 2362-generate-the-invoice
```

# Split Full Name into First/Middle/Last - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_name VARCHAR(30)
);

INSERT INTO customers (customer_name) VALUES
('Soumya Kole'),
('Akash Kumar Singh'),
('Tom');
```

Load this dataset:

```bash
make setup first-middle-last-name
```

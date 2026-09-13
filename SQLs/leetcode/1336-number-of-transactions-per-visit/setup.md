# 1336. Number of Transactions per Visit - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Visits;

CREATE TABLE Visits (
    user_id    INT,
    visit_date DATE,
    PRIMARY KEY (user_id, visit_date)
);

CREATE TABLE Transactions (
    user_id          INT,
    transaction_date DATE,
    amount           INT
);

INSERT INTO Visits (user_id, visit_date) VALUES
(1, '2020-01-01'),
(2, '2020-01-02'),
(12, '2020-01-01'),
(19, '2020-01-03'),
(1, '2020-01-02'),
(2, '2020-01-03'),
(1, '2020-01-04'),
(7, '2020-01-11'),
(9, '2020-01-25'),
(8, '2020-01-28');

INSERT INTO Transactions (user_id, transaction_date, amount) VALUES
(1, '2020-01-02', 120),
(2, '2020-01-03', 22),
(7, '2020-01-11', 232),
(1, '2020-01-04', 7),
(9, '2020-01-25', 33),
(9, '2020-01-25', 66),
(8, '2020-01-28', 1),
(9, '2020-01-25', 99);
```

Load this dataset:

```bash
make setup 1336-number-of-transactions-per-visit
```

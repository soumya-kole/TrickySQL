# 579. Find Cumulative Salary of an Employee - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    id     INT,
    month  INT,
    salary INT,
    PRIMARY KEY (id, month)
);

INSERT INTO Employee (id, month, salary) VALUES
(1, 1, 20),
(2, 1, 20),
(1, 2, 30),
(2, 2, 30),
(3, 2, 40),
(1, 3, 40),
(3, 3, 60),
(1, 4, 60),
(3, 4, 70),
(1, 7, 90),
(1, 8, 90);
```

Load this dataset:

```bash
make setup 0579-find-cumulative-salary-of-an-employee
```

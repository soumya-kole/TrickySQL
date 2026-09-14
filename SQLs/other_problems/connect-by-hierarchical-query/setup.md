# Hierarchical Query in MySQL (CONNECT BY equivalent) - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id         INT PRIMARY KEY,
    name       VARCHAR(255),
    manager_id INT
);

INSERT INTO employees (id, name, manager_id) VALUES
(1, 'CEO', NULL),
(2, 'CTO', 1),
(3, 'CFO', 1),
(4, 'Manager A', 1),
(5, 'Manager B', 1),
(6, 'Employee 1', 4),
(7, 'Employee 2', 4),
(8, 'Employee 3', 5),
(9, 'Employee 4', 5),
(10, 'Lead Developer', 2),
(11, 'Developer 1', 10),
(12, 'Developer 2', 10),
(13, 'Finance Manager', 3),
(14, 'Accountant 1', 13),
(15, 'Accountant 2', 13);
```

Load this dataset:

```bash
make setup connect-by-hierarchical-query
```

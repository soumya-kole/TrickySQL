# 1270. All People Report to the Given Manager - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Employees;

CREATE TABLE Employees (
    employee_id   INT PRIMARY KEY,
    employee_name VARCHAR(50),
    manager_id    INT
);

INSERT INTO Employees (employee_id, employee_name, manager_id) VALUES
(1, 'Boss', 1),
(3, 'Alice', 3),
(2, 'Bob', 1),
(4, 'Daniel', 2),
(7, 'Luis', 4),
(8, 'Jhon', 3),
(9, 'Angela', 8),
(77, 'Robert', 1);
```

Load this dataset:

```bash
make setup 1270-all-people-report-to-the-given-manager
```

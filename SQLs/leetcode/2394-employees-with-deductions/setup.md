# 2394. Employees With Deductions - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Logs;
DROP TABLE IF EXISTS Employees;

CREATE TABLE Employees (
    employee_id  INT PRIMARY KEY,
    needed_hours INT
);

CREATE TABLE Logs (
    employee_id INT,
    in_time     DATETIME,
    out_time    DATETIME,
    PRIMARY KEY (employee_id, in_time, out_time)
);

INSERT INTO Employees (employee_id, needed_hours) VALUES
(1, 20),
(2, 12),
(3, 2);

INSERT INTO Logs (employee_id, in_time, out_time) VALUES
(1, '2022-10-01 09:00:00', '2022-10-01 17:00:00'),
(1, '2022-10-06 09:05:04', '2022-10-06 17:09:03'),
(1, '2022-10-12 23:00:00', '2022-10-13 03:00:01'),
(2, '2022-10-29 12:00:00', '2022-10-29 23:58:58');
```

Load this dataset:

```bash
make setup 2394-employees-with-deductions
```

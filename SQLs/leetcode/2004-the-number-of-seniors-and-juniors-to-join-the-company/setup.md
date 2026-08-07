# 2004. The Number of Seniors and Juniors to Join the Company - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Candidates;

CREATE TABLE Candidates (
    employee_id INT PRIMARY KEY,
    experience  ENUM('Senior', 'Junior'),
    salary      INT
);

INSERT INTO Candidates (employee_id, experience, salary) VALUES
(1, 'Junior', 10000),
(9, 'Junior', 10000),
(2, 'Senior', 20000),
(11, 'Senior', 20000),
(13, 'Senior', 50000),
(4, 'Junior', 40000);
```

Load this dataset:

```bash
make setup 2004-the-number-of-seniors-and-juniors-to-join-the-company
```

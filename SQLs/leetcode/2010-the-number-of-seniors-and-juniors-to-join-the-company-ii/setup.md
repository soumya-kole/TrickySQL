# 2010. The Number of Seniors and Juniors to Join the Company II - Setup

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
(9, 'Junior', 15000),
(2, 'Senior', 20000),
(11, 'Senior', 16000),
(13, 'Senior', 50000),
(4, 'Junior', 40000);
```

Load this dataset:

```bash
make setup 2010-the-number-of-seniors-and-juniors-to-join-the-company-ii
```

## Setup2

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
(1, 'Junior', 25000),
(9, 'Junior', 10000),
(2, 'Senior', 85000),
(11, 'Senior', 80000),
(13, 'Senior', 90000),
(4, 'Junior', 30000);
```

Load this dataset:

```bash
make setup 2010-the-number-of-seniors-and-juniors-to-join-the-company-ii 2
```

## Setup3

Edge case: seniors' salaries sum to exactly the $70000 budget, leaving $0 for juniors.

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
(1, 'Senior', 30000),
(2, 'Senior', 40000),
(3, 'Senior', 50000),
(4, 'Junior', 5000),
(5, 'Junior', 3000);
```

Load this dataset:

```bash
make setup 2010-the-number-of-seniors-and-juniors-to-join-the-company-ii 3
```

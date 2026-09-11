# 1699. Number of Calls Between Two Persons - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Calls;

CREATE TABLE Calls (
    from_id  INT,
    to_id    INT,
    duration INT
);

INSERT INTO Calls (from_id, to_id, duration) VALUES
(1, 2, 59),
(2, 1, 11),
(1, 3, 20),
(3, 4, 100),
(3, 4, 200),
(3, 4, 200),
(4, 3, 499);
```

Load this dataset:

```bash
make setup 1699-number-of-calls-between-two-persons
```

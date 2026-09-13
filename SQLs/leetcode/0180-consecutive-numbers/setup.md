# 180. Consecutive Numbers - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Logs;

CREATE TABLE Logs (
    id  INT PRIMARY KEY,
    num VARCHAR(10)
);

INSERT INTO Logs (id, num) VALUES
(1, '1'),
(2, '1'),
(3, '1'),
(4, '2'),
(5, '1'),
(6, '2'),
(7, '2');
```

Load this dataset:

```bash
make setup 0180-consecutive-numbers
```

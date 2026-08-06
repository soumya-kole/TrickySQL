# 571. Find Median Given Frequency of Numbers - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Numbers;

CREATE TABLE Numbers (
    num       INT PRIMARY KEY,
    frequency INT
);

INSERT INTO Numbers (num, frequency) VALUES
(0, 7),
(1, 1),
(2, 3),
(3, 1);
```

Load this dataset:

```bash
make setup 0571-find-median-given-frequency-of-numbers
```

## Setup2

An odd-length dataset whose decompressed array is **not** already sorted by scan order.
It trips up the two classic mistakes at once: relying on implicit row order (no `ORDER BY`
in `ROW_NUMBER()`) and using a `CASE`/division that breaks for odd lengths.

Decompressed sorted array: `[0, 5, 100]` — total = 3 (odd), correct median `5.0`.

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Numbers;

CREATE TABLE Numbers (
    num       INT PRIMARY KEY,
    frequency INT
);

INSERT INTO Numbers (num, frequency) VALUES
(0, 1),
(5, 1),
(100, 1);
```

Load this dataset:

```bash
make setup 0571-find-median-given-frequency-of-numbers 2
```

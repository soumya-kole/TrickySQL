# 603. Consecutive Available Seats - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Cinema;

CREATE TABLE Cinema (
    seat_id INT PRIMARY KEY AUTO_INCREMENT,
    free    BOOL
);

INSERT INTO Cinema (seat_id, free) VALUES
(1, 1),
(2, 0),
(3, 1),
(4, 1),
(5, 1);
```

Load this dataset:

```bash
make setup 0603-consecutive-available-seats
```

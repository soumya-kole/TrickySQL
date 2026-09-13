# 1709. Biggest Window Between Visits - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS UserVisits;

CREATE TABLE UserVisits (
    user_id    INT,
    visit_date DATE
);

INSERT INTO UserVisits (user_id, visit_date) VALUES
(1, '2020-11-28'),
(1, '2020-10-20'),
(1, '2020-12-03'),
(2, '2020-10-05'),
(2, '2020-12-09'),
(3, '2020-11-11');
```

Load this dataset:

```bash
make setup 1709-biggest-window-between-visits
```

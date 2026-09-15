# 585. Investments in 2016 - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Insurance;

CREATE TABLE Insurance (
    pid      INT PRIMARY KEY,
    tiv_2015 FLOAT,
    tiv_2016 FLOAT,
    lat      FLOAT,
    lon      FLOAT
);

INSERT INTO Insurance (pid, tiv_2015, tiv_2016, lat, lon) VALUES
(1, 10, 5, 10, 10),
(2, 20, 20, 20, 20),
(3, 10, 30, 20, 20),
(4, 10, 40, 40, 40);
```

Load this dataset:

```bash
make setup 0585-investments-in-2016
```

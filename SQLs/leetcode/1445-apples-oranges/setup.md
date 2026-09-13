# 1445. Apples & Oranges - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Sales;

CREATE TABLE Sales (
    sale_date DATE,
    fruit     ENUM('apples', 'oranges'),
    sold_num  INT,
    PRIMARY KEY (sale_date, fruit)
);

INSERT INTO Sales (sale_date, fruit, sold_num) VALUES
('2020-05-01', 'apples', 10),
('2020-05-01', 'oranges', 8),
('2020-05-02', 'apples', 15),
('2020-05-02', 'oranges', 15),
('2020-05-03', 'apples', 20),
('2020-05-03', 'oranges', 0),
('2020-05-04', 'apples', 15),
('2020-05-04', 'oranges', 16);
```

Load this dataset:

```bash
make setup 1445-apples-oranges
```

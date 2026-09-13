# 612. Shortest Distance in a Plane - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Point2D;

CREATE TABLE Point2D (
    x INT,
    y INT,
    PRIMARY KEY (x, y)
);

INSERT INTO Point2D (x, y) VALUES
(-1, -1),
(0, 0),
(-1, -2);
```

Load this dataset:

```bash
make setup 0612-shortest-distance-in-a-plane
```

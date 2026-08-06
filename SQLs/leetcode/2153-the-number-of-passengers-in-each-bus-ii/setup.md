# 2153. The Number of Passengers in Each Bus II - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Buses;

CREATE TABLE Buses (
    bus_id       INT PRIMARY KEY,
    arrival_time INT,
    capacity     INT
);

CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    arrival_time INT
);

INSERT INTO Buses (bus_id, arrival_time, capacity) VALUES
(1, 2, 1),
(2, 4, 10),
(3, 7, 2);

INSERT INTO Passengers (passenger_id, arrival_time) VALUES
(11, 1),
(12, 1),
(13, 5),
(14, 6),
(15, 7);
```

Load this dataset:

```bash
make setup 2153-the-number-of-passengers-in-each-bus-ii
```

## Setup2

A "wasted capacity" dataset that breaks the naive `LEAST(total_capacity, total_waiting)`
shortcut. An early high-capacity bus arrives when almost nobody is waiting, so most of its
seats are wasted (not banked for later), and a later bus is capacity-limited.

```
+--------+--------------+----------+         +--------------+--------------+
| bus_id | arrival_time | capacity |         | passenger_id | arrival_time |
+--------+--------------+----------+         +--------------+--------------+
| 1      | 2            | 5        |         | 11           | 1            |
| 2      | 10           | 1        |         | 12           | 5            |
| 3      | 20           | 3        |         | 13           | 6            |
+--------+--------------+----------+         | 14           | 7            |
                                             | 15           | 8            |
                                             | 16           | 15           |
                                             +--------------+--------------+
```

- Bus 1 (t=2, cap 5): only passenger 11 has arrived → boards **1**, wastes 4 seats.
- Bus 2 (t=10, cap 1): 4 still waiting → boards **1**.
- Bus 3 (t=20, cap 3): 4 still waiting → boards **3**.

Expected `passengers_cnt`: `1, 1, 3` (total 5). The naive shortcut would give
`LEAST(9, 6) = 6` — wrong, because bus 1's 4 wasted seats are gone for good.

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Buses;

CREATE TABLE Buses (
    bus_id       INT PRIMARY KEY,
    arrival_time INT,
    capacity     INT
);

CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    arrival_time INT
);

INSERT INTO Buses (bus_id, arrival_time, capacity) VALUES
(1, 2, 5),
(2, 10, 1),
(3, 20, 3);

INSERT INTO Passengers (passenger_id, arrival_time) VALUES
(11, 1),
(12, 5),
(13, 6),
(14, 7),
(15, 8),
(16, 15);
```

Load this dataset:

```bash
make setup 2153-the-number-of-passengers-in-each-bus-ii 2
```

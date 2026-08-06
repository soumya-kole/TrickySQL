# 2142. The Number of Passengers in Each Bus I - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Buses;

CREATE TABLE Buses (
    bus_id       INT PRIMARY KEY,
    arrival_time INT
);

CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    arrival_time INT
);

INSERT INTO Buses (bus_id, arrival_time) VALUES
(1, 2),
(2, 4),
(3, 7);

INSERT INTO Passengers (passenger_id, arrival_time) VALUES
(11, 1),
(12, 5),
(13, 6),
(14, 7);
```

Load this dataset:

```bash
make setup 2142-the-number-of-passengers-in-each-bus-i
```

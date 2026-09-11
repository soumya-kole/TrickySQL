# 1635. Hopper Company Queries I - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS AcceptedRides;
DROP TABLE IF EXISTS Rides;
DROP TABLE IF EXISTS Drivers;

CREATE TABLE Drivers (
    driver_id INT PRIMARY KEY,
    join_date DATE
);

CREATE TABLE Rides (
    ride_id      INT PRIMARY KEY,
    user_id      INT,
    requested_at DATE
);

CREATE TABLE AcceptedRides (
    ride_id       INT PRIMARY KEY,
    driver_id     INT,
    ride_distance INT,
    ride_duration INT
);

INSERT INTO Drivers (driver_id, join_date) VALUES
(10, '2019-12-10'),
(8, '2020-01-13'),
(5, '2020-02-16'),
(7, '2020-03-08'),
(4, '2020-05-17'),
(1, '2020-10-24'),
(6, '2021-01-05');

INSERT INTO Rides (ride_id, user_id, requested_at) VALUES
(6, 75, '2019-12-09'),
(1, 54, '2020-02-09'),
(10, 63, '2020-03-04'),
(19, 39, '2020-04-06'),
(3, 41, '2020-06-03'),
(13, 52, '2020-06-22'),
(7, 69, '2020-07-16'),
(17, 70, '2020-08-25'),
(20, 81, '2020-11-02'),
(5, 57, '2020-11-09'),
(2, 42, '2020-12-09'),
(11, 68, '2021-01-11'),
(15, 32, '2021-01-17'),
(12, 11, '2021-01-19'),
(14, 18, '2021-01-27');

INSERT INTO AcceptedRides (ride_id, driver_id, ride_distance, ride_duration) VALUES
(10, 10, 63, 38),
(13, 10, 73, 96),
(7, 8, 100, 28),
(17, 7, 119, 68),
(20, 1, 121, 92),
(5, 7, 42, 101),
(2, 4, 6, 38),
(11, 8, 37, 43),
(15, 8, 108, 82),
(12, 8, 38, 34),
(14, 1, 90, 74);
```

Load this dataset:

```bash
make setup 1635-hopper-company-queries-i
```

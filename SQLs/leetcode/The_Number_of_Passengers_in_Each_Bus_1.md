
<!-- problem:start -->

# [2142. The Number of Passengers in Each Bus I 🔒](https://leetcode.com/problems/the-number-of-passengers-in-each-bus-i)


## Description

<!-- description:start -->

<p>Table: <code>Buses</code></p>

<pre>
+--------------+------+
| Column Name  | Type |
+--------------+------+
| bus_id       | int  |
| arrival_time | int  |
+--------------+------+
bus_id is the column with unique values for this table.
Each row of this table contains information about the arrival time of a bus at the LeetCode station.
No two buses will arrive at the same time.
</pre>

<p>&nbsp;</p>

<p>Table: <code>Passengers</code></p>

<pre>
+--------------+------+
| Column Name  | Type |
+--------------+------+
| passenger_id | int  |
| arrival_time | int  |
+--------------+------+
passenger_id is the column with unique values for this table.
Each row of this table contains information about the arrival time of a passenger at the LeetCode station.
</pre>

<p>&nbsp;</p>

<p>Buses and passengers arrive at the LeetCode station. If a bus arrives at the station at time <code>t<sub>bus</sub></code> and a passenger arrived at time <code>t<sub>passenger</sub></code> where <code>t<sub>passenger</sub> &lt;= t<sub>bus</sub></code> and the passenger did not catch any bus, the passenger will use that bus.</p>

<p>Write a solution&nbsp;to report the number of users that used each bus.</p>

<p>Return the result table ordered by <code>bus_id</code> in <strong>ascending order</strong>.</p>

<p>The&nbsp;result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> 
Buses table:
+--------+--------------+
| bus_id | arrival_time |
+--------+--------------+
| 1      | 2            |
| 2      | 4            |
| 3      | 7            |
+--------+--------------+
Passengers table:
+--------------+--------------+
| passenger_id | arrival_time |
+--------------+--------------+
| 11           | 1            |
| 12           | 5            |
| 13           | 6            |
| 14           | 7            |
+--------------+--------------+
<strong>Output:</strong> 
+--------+----------------+
| bus_id | passengers_cnt |
+--------+----------------+
| 1      | 1              |
| 2      | 0              |
| 3      | 3              |
+--------+----------------+
<strong>Explanation:</strong> 
- Passenger 11 arrives at time 1.
- Bus 1 arrives at time 2 and collects passenger 11.

- Bus 2 arrives at time 4 and does not collect any passengers.

- Passenger 12 arrives at time 5.
- Passenger 13 arrives at time 6.
- Passenger 14 arrives at time 7.
- Bus 3 arrives at time 7 and collects passengers 12, 13, and 14.
</pre>

<!-- description:end -->

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

## Solutions

<!-- solution:start -->

### Solution 1

<!-- tabs:start -->

#### MySQL

```sql
WITH passenger_bus AS (
    SELECT
        passenger_id,
        MIN(b.arrival_time) AS boarding_time
    FROM Passengers p
    JOIN Buses b
    WHERE p.arrival_time <= b.arrival_time
    GROUP BY p.passenger_id
)
SELECT
    b.bus_id,
    COUNT(p.passenger_id) AS passengers_cnt
FROM Buses b
LEFT JOIN passenger_bus p ON p.boarding_time = b.arrival_time
GROUP BY b.bus_id
ORDER BY b.bus_id;

```

<!-- tabs:end -->

<!-- solution:end -->

<!-- solution:start -->

### Solution 2

<!-- tabs:start -->

#### MySQL

```sql
WITH cte AS (
    SELECT
        *,
        LAG(b.arrival_time, 1) OVER (ORDER BY b.arrival_time) AS prev_bus
    FROM Buses b
)
SELECT
    c.bus_id,
    COUNT(p.passenger_id) AS passengers_cnt
FROM cte c
LEFT JOIN Passengers p
    ON p.arrival_time <= c.arrival_time
    AND p.arrival_time > COALESCE(c.prev_bus, 0)
GROUP BY 1
ORDER BY 1;
```

<!-- tabs:end -->

<!-- solution:end -->

<!-- problem:end -->
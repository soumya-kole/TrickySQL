<!-- problem:start -->

# [2153. The Number of Passengers in Each Bus II 🔒](https://leetcode.com/problems/the-number-of-passengers-in-each-bus-ii)


## Description

<!-- description:start -->

<p>Table: <code>Buses</code></p>

<pre>
+--------------+------+
| Column Name  | Type |
+--------------+------+
| bus_id       | int  |
| arrival_time | int  |
| capacity     | int  |
+--------------+------+
bus_id contains unique values.
Each row of this table contains information about the arrival time of a bus at the LeetCode station and its capacity (the number of empty seats it has).
No two buses will arrive at the same time and all bus capacities will be positive integers.
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
passenger_id contains unique values.
Each row of this table contains information about the arrival time of a passenger at the LeetCode station.
</pre>

<p>&nbsp;</p>

<p>Buses and passengers arrive at the LeetCode station. If a bus arrives at the station at a time <code>t<sub>bus</sub></code> and a passenger arrived at a time <code>t<sub>passenger</sub></code> where <code>t<sub>passenger</sub> &lt;= t<sub>bus</sub></code> and the passenger did not catch any bus, the passenger will use that bus. In addition, each bus has a capacity. If at the moment the bus arrives at the station there are more passengers waiting than its capacity <code>capacity</code>, only <code>capacity</code> passengers will use the bus.</p>

<p>Write a solution&nbsp;to report the number of users that used each bus.</p>

<p>Return the result table ordered by <code>bus_id</code> in <strong>ascending order</strong>.</p>

<p>The result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> 
Buses table:
+--------+--------------+----------+
| bus_id | arrival_time | capacity |
+--------+--------------+----------+
| 1      | 2            | 1        |
| 2      | 4            | 10       |
| 3      | 7            | 2        |
+--------+--------------+----------+
Passengers table:
+--------------+--------------+
| passenger_id | arrival_time |
+--------------+--------------+
| 11           | 1            |
| 12           | 1            |
| 13           | 5            |
| 14           | 6            |
| 15           | 7            |
+--------------+--------------+
<strong>Output:</strong> 
+--------+----------------+
| bus_id | passengers_cnt |
+--------+----------------+
| 1      | 1              |
| 2      | 1              |
| 3      | 2              |
+--------+----------------+
<strong>Explanation:</strong> 
- Passenger 11 arrives at time 1.
- Passenger 12 arrives at time 1.
- Bus 1 arrives at time 2 and collects passenger 11 as it has one empty seat.

- Bus 2 arrives at time 4 and collects passenger 12 as it has ten empty seats.

- Passenger 12 arrives at time 5.
- Passenger 13 arrives at time 6.
- Passenger 14 arrives at time 7.
- Bus 3 arrives at time 7 and collects passengers 12 and 13 as it has two empty seats.
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

## Solutions

### Core idea

Process buses in arrival order. At each bus, the number of passengers **waiting** is every passenger who has arrived (`arrival_time <= bus arrival_time`) and hasn't already boarded an earlier bus. A bus boards `LEAST(capacity, waiting)` of them.

The key quantity is the **running total of passengers already onboarded** across all earlier buses. If we call it `cum`, then for each bus:

```
boarded_i = LEAST(capacity_i, waiting_i - cum_{i-1})
cum_i     = cum_{i-1} + boarded_i
```

Both solutions below compute the same `cum`; they differ only in how.

<!-- solution:start -->

### Solution 1: Recursive CTE

Carry the running total `cum` forward one bus at a time, then recover each bus's individual count with `LAG` at the end.

<!-- tabs:start -->

#### MySQL

```sql
WITH RECURSIVE
src AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY arrival_time) AS rn,
        bus_id,
        capacity,
        (SELECT COUNT(*) FROM Passengers p WHERE p.arrival_time <= b.arrival_time) AS waiting
    FROM Buses b
),
run AS (
    -- Anchor: the first bus boards LEAST(capacity, waiting)
    SELECT rn, bus_id, LEAST(capacity, waiting) AS cum
    FROM src
    WHERE rn = 1

    UNION ALL

    -- Recursive step: add this bus's boarding to the running total
    SELECT s.rn, s.bus_id,
           r.cum + LEAST(s.capacity, s.waiting - r.cum)
    FROM run r
    JOIN src s ON s.rn = r.rn + 1
)
SELECT
    bus_id,
    cum - LAG(cum, 1, 0) OVER (ORDER BY rn) AS passengers_cnt
FROM run
ORDER BY bus_id;
```

<!-- tabs:end -->

**Step by step:**

1. **`src`** — number the buses `rn = 1, 2, 3, …` in arrival order, and for each bus count `waiting` = total passengers who have arrived by that bus's time (a correlated `COUNT`).
2. **Anchor (`rn = 1`)** — the first bus has no prior buses, so `cum = LEAST(capacity, waiting)`.
3. **Recursive step** — join the previous result row (`r`) to the next bus (`s.rn = r.rn + 1`). The next bus boards `LEAST(capacity, waiting - r.cum)` (remaining waiting passengers), and we accumulate that into `cum`. Only **one** column (`cum`) is carried forward.
4. **Final `SELECT`** — each bus's own count is `cum_i - cum_{i-1}`, recovered with `LAG(cum, 1, 0)` (the `0` default handles the first bus).

### Solution 2: Window functions (no recursion)

The recurrence `cum_i = MIN(waiting_i, cum_{i-1} + cap_i)` can be unrolled into a closed form. Writing `C_i` for the running capacity sum:

```
cum_i = C_i + LEAST(0, MIN over k <= i of (waiting_k - C_k))
```

The inner `MIN` is a running minimum — a window function — so no row-by-row recursion is needed.

> **Careful:** the naive `LEAST(total capacity, total waiting)` does **not** work here, because a bus's unused seats are wasted rather than banked for later buses. The running-minimum form above accounts for that.

<!-- tabs:start -->

#### MySQL

```sql
WITH src AS (
    SELECT
        bus_id,
        arrival_time,
        SUM(capacity) OVER (ORDER BY arrival_time) AS cum_cap,
        (SELECT COUNT(*) FROM Passengers p WHERE p.arrival_time <= b.arrival_time) AS waiting
    FROM Buses b
),
cum AS (
    SELECT
        bus_id,
        arrival_time,
        cum_cap + LEAST(0, MIN(waiting - cum_cap) OVER (ORDER BY arrival_time)) AS boarded
    FROM src
)
SELECT
    bus_id,
    boarded - LAG(boarded, 1, 0) OVER (ORDER BY arrival_time) AS passengers_cnt
FROM cum
ORDER BY bus_id;
```

<!-- tabs:end -->

**Step by step:**

1. **`src`** — for each bus compute `cum_cap` = running sum of capacities up to this bus, and `waiting` = passengers arrived by this bus's time.
2. **`cum`** — the total onboarded through bus `i` is `cum_cap + LEAST(0, running_min(waiting - cum_cap))`. The running minimum captures the most binding earlier bottleneck: at some earlier bus, passengers may have run out relative to seats offered, and that wasted capacity is permanently lost — which is exactly what subtracting the running min accounts for.
3. **Final `SELECT`** — each bus's own count is the difference between consecutive cumulative totals, via `LAG(boarded, 1, 0)`.

> Both queries return `1, 1, 2` for the example. Solution 2 avoids recursion and runs in a single pass; Solution 1 is the more direct, easier-to-read greedy translation.

<!-- solution:end -->

<!-- problem:end -->
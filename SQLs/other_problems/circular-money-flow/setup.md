# Circular Money Flow - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id   INT PRIMARY KEY,
    sender_id        VARCHAR(3) NOT NULL,
    receiver_id      VARCHAR(3) NOT NULL,
    amount           INT NOT NULL,
    transaction_time DATETIME NOT NULL
);

INSERT INTO transactions VALUES
(1, '101', '102', 500,  '2025-01-01 09:00:00'),
(2, '102', '103', 500,  '2025-01-01 09:10:00'),
(3, '103', '101', 500,  '2025-01-01 09:20:00'),
(4, '201', '202', 1000, '2025-01-01 10:00:00'),
(5, '202', '203', 1000, '2025-01-01 10:05:00'),
(6, '203', '204', 1000, '2025-01-01 10:10:00');
```

Load this dataset:

```bash
make setup circular-money-flow
```

## Setup2

An edge-case dataset that checks every rule. The default data doesn't test these,
because its only loop already satisfies all of them.

- **101 → 102 → 103 → 101** (500, 20 min): a valid cycle, as in the default data.
- **301 → 302 → 303 → 301**: the last transfer is 650 instead of 700 → *not* a cycle (rule 5).
- **401 → 402 → 403 → 401** (400): the loop closes 65 min after it starts → *not* a cycle (rule 4).
- **501 → 502 → 501** (200, 30 min): a valid cycle with a single intermediate user (rule 2).
- **601 → 602 → 603 → 602 → 601** (300, 30 min): a valid cycle that visits intermediate
  user 602 twice (rule 7). It also contains two shorter cycles, which are reported too:
  **601 → 602 → 601** (txns 12, 15) and **602 → 603 → 602** (txns 13, 14).

Expected output, with `cycle_id` following each cycle's first transfer time, then path:

```
+----------+-------------------------+--------+--------------+
| cycle_id | path                    | amount | cycle_length |
+----------+-------------------------+--------+--------------+
| 1        | 101->102->103->101      | 500    | 3            |
| 2        | 501->502->501           | 200    | 2            |
| 3        | 601->602->601           | 300    | 2            |
| 4        | 601->602->603->602->601 | 300    | 4            |
| 5        | 602->603->602           | 300    | 2            |
+----------+-------------------------+--------+--------------+
```

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id   INT PRIMARY KEY,
    sender_id        VARCHAR(3) NOT NULL,
    receiver_id      VARCHAR(3) NOT NULL,
    amount           INT NOT NULL,
    transaction_time DATETIME NOT NULL
);

INSERT INTO transactions VALUES
(1,  '101', '102', 500, '2025-01-01 09:00:00'),
(2,  '102', '103', 500, '2025-01-01 09:10:00'),
(3,  '103', '101', 500, '2025-01-01 09:20:00'),
(4,  '301', '302', 700, '2025-01-01 10:00:00'),
(5,  '302', '303', 700, '2025-01-01 10:10:00'),
(6,  '303', '301', 650, '2025-01-01 10:20:00'),
(7,  '401', '402', 400, '2025-01-01 11:00:00'),
(8,  '402', '403', 400, '2025-01-01 11:40:00'),
(9,  '403', '401', 400, '2025-01-01 12:05:00'),
(10, '501', '502', 200, '2025-01-01 12:30:00'),
(11, '502', '501', 200, '2025-01-01 13:00:00'),
(12, '601', '602', 300, '2025-01-01 14:00:00'),
(13, '602', '603', 300, '2025-01-01 14:10:00'),
(14, '603', '602', 300, '2025-01-01 14:20:00'),
(15, '602', '601', 300, '2025-01-01 14:30:00');
```

Load this dataset:

```bash
make setup circular-money-flow 2
```

## Setup3

The starting user keeps sending money after their loop has closed (rule 7):

- **101 → 102 → 103 → 101** (txns 1–3, 09:00–09:20): a valid cycle.
- **101 → 104 → 101** (txns 4–5, 09:30–09:40): a second valid cycle for 101.
- **101 → 102 → 103 → 101 → 104 → 101**: all 5 transfers are in time order, within 1 hour
  and for the same amount, and the path ends back at 101. But 101 also appears in the
  middle → *not* a cycle. It is two loops joined at 101.

A query that only checks the path's end user (`start_user = receiver_id`) wrongly reports
the 5-step path. The start user's middle appearances have to be checked as well.

Expected output:

```
+----------+--------------------+--------+--------------+
| cycle_id | path               | amount | cycle_length |
+----------+--------------------+--------+--------------+
| 1        | 101->102->103->101 | 500    | 3            |
| 2        | 101->104->101      | 500    | 2            |
+----------+--------------------+--------+--------------+
```

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id   INT PRIMARY KEY,
    sender_id        VARCHAR(3) NOT NULL,
    receiver_id      VARCHAR(3) NOT NULL,
    amount           INT NOT NULL,
    transaction_time DATETIME NOT NULL
);

INSERT INTO transactions VALUES
(1, '101', '102', 500, '2025-01-01 09:00:00'),
(2, '102', '103', 500, '2025-01-01 09:10:00'),
(3, '103', '101', 500, '2025-01-01 09:20:00'),
(4, '101', '104', 500, '2025-01-01 09:30:00'),
(5, '104', '101', 500, '2025-01-01 09:40:00');
```

Load this dataset:

```bash
make setup circular-money-flow 3
```

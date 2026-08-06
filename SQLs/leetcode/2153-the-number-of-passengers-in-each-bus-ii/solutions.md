# 2153. The Number of Passengers in Each Bus II - Solutions

## Core idea

Process buses in arrival order. At each bus, the number of passengers **waiting** is every passenger who has arrived (`arrival_time <= bus arrival_time`) and hasn't already boarded an earlier bus. A bus boards `LEAST(capacity, waiting)` of them.

The key quantity is the **running total of passengers already onboarded** across all earlier buses. If we call it `cum`, then for each bus:

```
boarded_i = LEAST(capacity_i, waiting_i - cum_{i-1})
cum_i     = cum_{i-1} + boarded_i
```

Both solutions below compute the same `cum`; they differ only in how.

## Solution 1: Recursive CTE

Carry the running total `cum` forward one bus at a time, then recover each bus's individual count with `LAG` at the end.

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

**Step by step:**

1. **`src`** — number the buses `rn = 1, 2, 3, …` in arrival order, and for each bus count `waiting` = total passengers who have arrived by that bus's time (a correlated `COUNT`).
2. **Anchor (`rn = 1`)** — the first bus has no prior buses, so `cum = LEAST(capacity, waiting)`.
3. **Recursive step** — join the previous result row (`r`) to the next bus (`s.rn = r.rn + 1`). The next bus boards `LEAST(capacity, waiting - r.cum)` (remaining waiting passengers), and we accumulate that into `cum`. Only **one** column (`cum`) is carried forward.
4. **Final `SELECT`** — each bus's own count is `cum_i - cum_{i-1}`, recovered with `LAG(cum, 1, 0)` (the `0` default handles the first bus).

## Solution 2: Window functions (no recursion)

The recurrence `cum_i = MIN(waiting_i, cum_{i-1} + cap_i)` can be unrolled into a closed form. Writing `C_i` for the running capacity sum:

```
cum_i = C_i + LEAST(0, MIN over k <= i of (waiting_k - C_k))
```

The inner `MIN` is a running minimum — a window function — so no row-by-row recursion is needed.

> **Careful:** the naive `LEAST(total capacity, total waiting)` does **not** work here, because a bus's unused seats are wasted rather than banked for later buses. The running-minimum form above accounts for that.

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

**Step by step:**

1. **`src`** — for each bus compute `cum_cap` = running sum of capacities up to this bus, and `waiting` = passengers arrived by this bus's time.
2. **`cum`** — the total onboarded through bus `i` is `cum_cap + LEAST(0, running_min(waiting - cum_cap))`. The running minimum captures the most binding earlier bottleneck: at some earlier bus, passengers may have run out relative to seats offered, and that wasted capacity is permanently lost — which is exactly what subtracting the running min accounts for.
3. **Final `SELECT`** — each bus's own count is the difference between consecutive cumulative totals, via `LAG(boarded, 1, 0)`.

> Both queries return `1, 1, 2` for the example. Solution 2 avoids recursion and runs in a single pass; Solution 1 is the more direct, easier-to-read greedy translation.

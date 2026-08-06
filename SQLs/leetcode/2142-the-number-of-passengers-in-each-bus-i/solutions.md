# 2142. The Number of Passengers in Each Bus I - Solutions

## Solution 1

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

## Solution 2

#### MySQL

```sql
WITH cte AS (
    SELECT
        *,
        COALESCE(LAG(b.arrival_time, 1) OVER (ORDER BY b.arrival_time), 0) AS prev_bus
    FROM Buses b
)
SELECT
    c.bus_id,
    COUNT(p.passenger_id) AS passengers_cnt
FROM cte c
LEFT JOIN Passengers p
    ON p.arrival_time > c.prev_bus
    AND p.arrival_time <= c.arrival_time
GROUP BY 1
ORDER BY 1;
```

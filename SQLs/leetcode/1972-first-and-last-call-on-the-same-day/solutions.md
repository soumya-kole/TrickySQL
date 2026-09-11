# 1972. First and Last Call On the Same Day - Solutions

## Solution 1

Each call is symmetric (`caller_id`/`recipient_id` both count as participants), so
the `Calls` rows are first doubled into a `caller_id -> recipient_id` view from
both directions with `UNION ALL`. Then, for each `(day, user)` partition,
`FIRST_VALUE()` picks the counterpart of that user's earliest call of the day
(ordered ascending) and their latest call of the day (ordered descending). A user
qualifies whenever those two counterparts are the same person.

#### MySQL

```sql
WITH s AS (
    SELECT caller_id, recipient_id, call_time
    FROM Calls

    UNION ALL

    SELECT recipient_id AS caller_id, caller_id AS recipient_id, call_time
    FROM Calls
),
t AS (
    SELECT
        caller_id AS user_id,
        FIRST_VALUE(recipient_id) OVER (
            PARTITION BY DATE(call_time), caller_id
            ORDER BY call_time ASC
        ) AS first_call,
        FIRST_VALUE(recipient_id) OVER (
            PARTITION BY DATE(call_time), caller_id
            ORDER BY call_time DESC
        ) AS last_call
    FROM s
)
SELECT DISTINCT user_id
FROM t
WHERE first_call = last_call;
```

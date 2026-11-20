# Circular Money Flow - Solutions

## Solution 1: Recursive CTE

Treat each transaction as a directed edge `sender → receiver` and walk the graph with a
recursive CTE, starting a chain from every transaction. Each row of the CTE carries the
transaction it just followed (`transaction_id`, `sender_id`, `receiver_id`,
`transaction_time`), plus the chain's starting user, start time, running path (`cycle`)
and `cycle_length`.

- **Anchor:** each transaction starts a chain of length 1.
- **Recursive step:** extend a chain by one transfer `t` when:
  - `t.sender_id` is the chain's last receiver (the money moves on),
  - `t.amount` matches the chain's amount (rule 5),
  - `t` happens after the previous transfer (rule 6), and no later than 1 hour after the
    chain's first transfer (rule 4).
- **Stop:** once a chain returns to its starting user it is a finished cycle, so
  `cte.receiver_id <> cte.start_user` stops it from being extended further. This keeps the
  starting user at the ends only (rule 7). Without it, `101->102->103->101->104->101` would
  be reported, which is two loops joined at 101. The loop `101->104->101` is still found by
  the chain that starts at the `101 → 104` transfer.
- **Final filter:** keep chains that end at the starting user. `cycle_length >= 2`
  requires at least one intermediate user (rule 2), which rules out a self-transfer
  `A → A`.

Intermediate users are not checked, so a cycle may revisit one, as in
`601->602->603->602->601`. The shorter cycles inside it (`601->602->601`,
`602->603->602`) are separate chains, so they are reported too.

The recursion always ends, even though users may repeat: every step must be strictly later
than the last and within the 1-hour window. Requiring each transfer to happen after the
previous one also means each cycle is found only once. For example, `102->103->101->102`
would need the 09:00 transfer `101 → 102` to happen after the 09:20 transfer `103 → 101`.

The 1-hour check compares full timestamps with `ADDDATE(start_time, INTERVAL 1 HOUR)`.
`TIMESTAMPDIFF(MINUTE, …) <= 60` would ignore leftover seconds, so a gap of 60 min 59 s
would count as 60 and pass.

The `CAST` in the anchor is required. The anchor sets each column's type for the whole
recursive CTE. Without the cast, `cycle` would be `VARCHAR(8)` (two `VARCHAR(3)` ids plus
`'->'`), and the first longer path fails with `Data too long for column 'cycle'` in strict
mode, or is silently cut short without it.

#### MySQL

```sql
WITH RECURSIVE cte AS (
    SELECT
        transaction_id,
        sender_id AS start_user,
        sender_id,
        receiver_id,
        amount,
        transaction_time AS start_time,
        transaction_time,
        CAST(CONCAT(sender_id, '->', receiver_id) AS CHAR(1000)) AS cycle,
        1 AS cycle_length
    FROM transactions
    UNION ALL
    SELECT
        t.transaction_id,
        cte.start_user,
        t.sender_id,
        t.receiver_id,
        t.amount,
        cte.start_time,
        t.transaction_time,
        CONCAT(cte.cycle, '->', t.receiver_id),
        cte.cycle_length + 1
    FROM cte
    JOIN transactions t
        ON cte.receiver_id = t.sender_id
       AND cte.amount = t.amount
       AND t.transaction_time > cte.transaction_time
       AND t.transaction_time <= ADDDATE(cte.start_time, INTERVAL 1 HOUR)
    WHERE cte.receiver_id <> cte.start_user
)
SELECT
    ROW_NUMBER() OVER (ORDER BY start_time, cycle) AS cycle_id,
    cycle AS path,
    amount,
    cycle_length
FROM cte
WHERE start_user = receiver_id
  AND cycle_length >= 2
ORDER BY cycle_id;
```

## Output

`## Setup`:

```
+----------+--------------------+--------+--------------+
| cycle_id | path               | amount | cycle_length |
+----------+--------------------+--------+--------------+
|        1 | 101->102->103->101 |    500 |            3 |
+----------+--------------------+--------+--------------+
```

`## Setup2`:

```
+----------+-------------------------+--------+--------------+
| cycle_id | path                    | amount | cycle_length |
+----------+-------------------------+--------+--------------+
|        1 | 101->102->103->101      |    500 |            3 |
|        2 | 501->502->501           |    200 |            2 |
|        3 | 601->602->601           |    300 |            2 |
|        4 | 601->602->603->602->601 |    300 |            4 |
|        5 | 602->603->602           |    300 |            2 |
+----------+-------------------------+--------+--------------+
```

`## Setup3`:

```
+----------+--------------------+--------+--------------+
| cycle_id | path               | amount | cycle_length |
+----------+--------------------+--------+--------------+
|        1 | 101->102->103->101 |    500 |            3 |
|        2 | 101->104->101      |    500 |            2 |
+----------+--------------------+--------+--------------+
```

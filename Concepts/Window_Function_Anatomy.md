# Anatomy of a Window Function

Every window function call is built from the same five layers. Each layer narrows or
orders the set of rows the function can "see" for a given output row:

```
Function()
  ↓
OVER()
  ↓
PARTITION BY   → separate running total per group
  ↓
ORDER BY       → establishes sequence
  ↓
ROWS BETWEEN   → defines how much history to include
```

This tutorial adds one layer at a time on the same tiny dataset so you can watch the
output change. Load the data with:

```bash
make setup Window_Function_Anatomy.md
```

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id        INT PRIMARY KEY,
    region    VARCHAR(10),
    sale_date DATE,
    amount    INT
);

INSERT INTO sales (id, region, sale_date, amount) VALUES
(1, 'East', '2024-01-01', 100),
(2, 'East', '2024-01-02', 200),
(3, 'East', '2024-01-03', 150),
(4, 'East', '2024-01-03',  50),
(5, 'East', '2024-01-04', 300),
(6, 'West', '2024-01-01',  80),
(7, 'West', '2024-01-02', 120),
(8, 'West', '2024-01-03', 200),
(9, 'West', '2024-01-04', 100);
```

Note rows 3 and 4: two `East` sales on the same date. That tie is deliberate — it is
what separates `ORDER BY` alone from an explicit `ROWS BETWEEN` frame in Step 5.

## Step 1: `Function()` — aggregate vs window

A plain aggregate collapses the table to one row:

```sql
SELECT SUM(amount) AS total FROM sales;
```

```
+-------+
| total |
+-------+
|  1300 |
+-------+
```

Adding `OVER()` turns the same function into a **window function**: every input row
survives, and the aggregate is computed *alongside* it rather than *instead of* it.

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER () AS total
FROM sales;
```

```
+----+--------+------------+--------+-------+
| id | region | sale_date  | amount | total |
+----+--------+------------+--------+-------+
|  1 | East   | 2024-01-01 |    100 |  1300 |
|  2 | East   | 2024-01-02 |    200 |  1300 |
|  3 | East   | 2024-01-03 |    150 |  1300 |
|  4 | East   | 2024-01-03 |     50 |  1300 |
|  5 | East   | 2024-01-04 |    300 |  1300 |
|  6 | West   | 2024-01-01 |     80 |  1300 |
|  7 | West   | 2024-01-02 |    120 |  1300 |
|  8 | West   | 2024-01-03 |    200 |  1300 |
|  9 | West   | 2024-01-04 |    100 |  1300 |
+----+--------+------------+--------+-------+
```

Any aggregate (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) can be used this way. Ranking
functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) and value functions (`LAG`, `LEAD`,
`FIRST_VALUE`, `LAST_VALUE`) *only* exist as window functions — they require `OVER`.

## Step 2: `OVER()` — the window

`OVER()` declares the set of rows the function works on. Empty parentheses mean
"the whole result set is one window", which is why every row above shows the same
1300. Everything that follows lives *inside* `OVER(...)` and shrinks or orders that
window.

A useful way to read it: for each output row, the function is evaluated against a
**window** of rows chosen by `PARTITION BY`, sequenced by `ORDER BY`, and trimmed by
the frame clause (`ROWS BETWEEN`).

## Step 3: `PARTITION BY` — one window per group

`PARTITION BY` splits the rows into independent groups. The function restarts in
every group, but unlike `GROUP BY` the rows are not collapsed.

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER (PARTITION BY region) AS region_total
FROM sales;
```

```
+----+--------+------------+--------+--------------+
| id | region | sale_date  | amount | region_total |
+----+--------+------------+--------+--------------+
|  1 | East   | 2024-01-01 |    100 |          800 |
|  2 | East   | 2024-01-02 |    200 |          800 |
|  3 | East   | 2024-01-03 |    150 |          800 |
|  4 | East   | 2024-01-03 |     50 |          800 |
|  5 | East   | 2024-01-04 |    300 |          800 |
|  6 | West   | 2024-01-01 |     80 |          500 |
|  7 | West   | 2024-01-02 |    120 |          500 |
|  8 | West   | 2024-01-03 |    200 |          500 |
|  9 | West   | 2024-01-04 |    100 |          500 |
+----+--------+------------+--------+--------------+
```

Compare with `GROUP BY region`, which would return just two rows. `PARTITION BY`
gives you the group total *and* keeps the detail — handy for "what % of its region
does this sale represent":

```sql
SELECT id, region, amount,
       ROUND(100.0 * amount / SUM(amount) OVER (PARTITION BY region), 1) AS pct_of_region
FROM sales;
```

```
+----+--------+--------+---------------+
| id | region | amount | pct_of_region |
+----+--------+--------+---------------+
|  1 | East   |    100 |          12.5 |
|  2 | East   |    200 |          25.0 |
|  3 | East   |    150 |          18.8 |
|  4 | East   |     50 |           6.3 |
|  5 | East   |    300 |          37.5 |
|  6 | West   |     80 |          16.0 |
|  7 | West   |    120 |          24.0 |
|  8 | West   |    200 |          40.0 |
|  9 | West   |    100 |          20.0 |
+----+--------+--------+---------------+
```

There is still no notion of "before" or "after" here — every row in a partition sees
the entire partition.

## Step 4: `ORDER BY` — establishing a sequence

Adding `ORDER BY` inside `OVER` does two things: it defines the sequence of rows within
each partition, **and it silently changes the frame**. Without `ORDER BY` the frame is
the whole partition; with `ORDER BY` the default frame becomes

```
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

— "from the start of the partition up to the current row". That is what turns a
partition total into a running total:

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER (PARTITION BY region ORDER BY sale_date) AS running_total
FROM sales;
```

```
+----+--------+------------+--------+---------------+
| id | region | sale_date  | amount | running_total |
+----+--------+------------+--------+---------------+
|  1 | East   | 2024-01-01 |    100 |           100 |
|  2 | East   | 2024-01-02 |    200 |           300 |
|  3 | East   | 2024-01-03 |    150 |           500 |
|  4 | East   | 2024-01-03 |     50 |           500 |
|  5 | East   | 2024-01-04 |    300 |           800 |
|  6 | West   | 2024-01-01 |     80 |            80 |
|  7 | West   | 2024-01-02 |    120 |           200 |
|  8 | West   | 2024-01-03 |    200 |           400 |
|  9 | West   | 2024-01-04 |    100 |           500 |
+----+--------+------------+--------+---------------+
```

Look at rows 3 and 4. Both are on `2024-01-03` and both show `500`. With `RANGE`, the
frame boundary is a *value*, not a row position: "current row" means "every row whose
`sale_date` equals mine". Tied rows (peers) are always included together, so the total
jumps from 300 straight to 500 for both.

That is often *not* what people expect from a "running total". Fixing it is exactly
what the frame clause is for.

`ORDER BY` is also what gives meaning to the sequence-aware functions:

```sql
SELECT id, region, sale_date, amount,
       ROW_NUMBER() OVER (PARTITION BY region ORDER BY sale_date, id) AS rn,
       LAG(amount)  OVER (PARTITION BY region ORDER BY sale_date, id) AS prev_amount,
       amount - LAG(amount) OVER (PARTITION BY region ORDER BY sale_date, id) AS delta
FROM sales;
```

```
+----+--------+------------+--------+----+-------------+-------+
| id | region | sale_date  | amount | rn | prev_amount | delta |
+----+--------+------------+--------+----+-------------+-------+
|  1 | East   | 2024-01-01 |    100 |  1 |        NULL |  NULL |
|  2 | East   | 2024-01-02 |    200 |  2 |         100 |   100 |
|  3 | East   | 2024-01-03 |    150 |  3 |         200 |   -50 |
|  4 | East   | 2024-01-03 |     50 |  4 |         150 |  -100 |
|  5 | East   | 2024-01-04 |    300 |  5 |          50 |   250 |
|  6 | West   | 2024-01-01 |     80 |  1 |        NULL |  NULL |
|  7 | West   | 2024-01-02 |    120 |  2 |          80 |    40 |
|  8 | West   | 2024-01-03 |    200 |  3 |         120 |    80 |
|  9 | West   | 2024-01-04 |    100 |  4 |         200 |  -100 |
+----+--------+------------+--------+----+-------------+-------+
```

Notice the `, id` tiebreaker. Whenever the `ORDER BY` column can have duplicates, add
a unique column so results are deterministic.

## Step 5: `ROWS BETWEEN` — how much history to include

The frame clause says which rows, relative to the current one, the function may see.
The general shape is:

```
ROWS BETWEEN <start> AND <end>
```

where each bound is one of:

| Bound                 | Meaning                              |
|-----------------------|--------------------------------------|
| `UNBOUNDED PRECEDING` | first row of the partition           |
| `n PRECEDING`         | n rows before the current row        |
| `CURRENT ROW`         | the current row itself               |
| `n FOLLOWING`         | n rows after the current row         |
| `UNBOUNDED FOLLOWING` | last row of the partition            |

### 5a. Row-by-row running total (fixing the tie)

`ROWS` counts physical rows, so the tied rows are no longer lumped together:

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER (
           PARTITION BY region ORDER BY sale_date, id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sales;
```

```
+----+--------+------------+--------+---------------+
| id | region | sale_date  | amount | running_total |
+----+--------+------------+--------+---------------+
|  1 | East   | 2024-01-01 |    100 |           100 |
|  2 | East   | 2024-01-02 |    200 |           300 |
|  3 | East   | 2024-01-03 |    150 |           450 |
|  4 | East   | 2024-01-03 |     50 |           500 |
|  5 | East   | 2024-01-04 |    300 |           800 |
|  6 | West   | 2024-01-01 |     80 |            80 |
|  7 | West   | 2024-01-02 |    120 |           200 |
|  8 | West   | 2024-01-03 |    200 |           400 |
|  9 | West   | 2024-01-04 |    100 |           500 |
+----+--------+------------+--------+---------------+
```

Row 3 is now `450` and row 4 is `500` — a true row-by-row accumulation. The `RANGE`
default and the explicit `ROWS` frame only differ when there are ties, which is exactly
when the difference bites.

### 5b. Sliding window — moving average of the last 3 sales

```sql
SELECT id, region, sale_date, amount,
       ROUND(AVG(amount) OVER (
           PARTITION BY region ORDER BY sale_date, id
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 2) AS moving_avg_3
FROM sales;
```

```
+----+--------+------------+--------+--------------+
| id | region | sale_date  | amount | moving_avg_3 |
+----+--------+------------+--------+--------------+
|  1 | East   | 2024-01-01 |    100 |       100.00 |
|  2 | East   | 2024-01-02 |    200 |       150.00 |
|  3 | East   | 2024-01-03 |    150 |       150.00 |
|  4 | East   | 2024-01-03 |     50 |       133.33 |
|  5 | East   | 2024-01-04 |    300 |       166.67 |
|  6 | West   | 2024-01-01 |     80 |        80.00 |
|  7 | West   | 2024-01-02 |    120 |       100.00 |
|  8 | West   | 2024-01-03 |    200 |       133.33 |
|  9 | West   | 2024-01-04 |    100 |       140.00 |
+----+--------+------------+--------+--------------+
```

The first two rows of each partition average over fewer than 3 rows because there is
no earlier history — the frame is clipped at the partition boundary, not padded.

### 5c. Centered window — previous, current and next

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER (
           PARTITION BY region ORDER BY sale_date, id
           ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       ) AS neighbour_sum
FROM sales;
```

```
+----+--------+------------+--------+---------------+
| id | region | sale_date  | amount | neighbour_sum |
+----+--------+------------+--------+---------------+
|  1 | East   | 2024-01-01 |    100 |           300 |
|  2 | East   | 2024-01-02 |    200 |           450 |
|  3 | East   | 2024-01-03 |    150 |           400 |
|  4 | East   | 2024-01-03 |     50 |           500 |
|  5 | East   | 2024-01-04 |    300 |           350 |
|  6 | West   | 2024-01-01 |     80 |           200 |
|  7 | West   | 2024-01-02 |    120 |           400 |
|  8 | West   | 2024-01-03 |    200 |           420 |
|  9 | West   | 2024-01-04 |    100 |           300 |
+----+--------+------------+--------+---------------+
```

### 5d. Looking forward — remaining amount

Frames can start at the current row and extend to the end:

```sql
SELECT id, region, sale_date, amount,
       SUM(amount) OVER (
           PARTITION BY region ORDER BY sale_date, id
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS remaining
FROM sales;
```

```
+----+--------+------------+--------+-----------+
| id | region | sale_date  | amount | remaining |
+----+--------+------------+--------+-----------+
|  1 | East   | 2024-01-01 |    100 |       800 |
|  2 | East   | 2024-01-02 |    200 |       700 |
|  3 | East   | 2024-01-03 |    150 |       500 |
|  4 | East   | 2024-01-03 |     50 |       350 |
|  5 | East   | 2024-01-04 |    300 |       300 |
|  6 | West   | 2024-01-01 |     80 |       500 |
|  7 | West   | 2024-01-02 |    120 |       420 |
|  8 | West   | 2024-01-03 |    200 |       300 |
|  9 | West   | 2024-01-04 |    100 |       100 |
+----+--------+------------+--------+-----------+
```

### 5e. The classic trap: `LAST_VALUE` with the default frame

Because the default frame ends at `CURRENT ROW`, `LAST_VALUE` looks like it is broken
unless you widen the frame:

```sql
SELECT id, region, sale_date, amount,
       FIRST_VALUE(amount) OVER (PARTITION BY region ORDER BY sale_date, id) AS first_ok,
       LAST_VALUE(amount)  OVER (PARTITION BY region ORDER BY sale_date, id) AS last_wrong,
       LAST_VALUE(amount)  OVER (
           PARTITION BY region ORDER BY sale_date, id
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_ok,
       FIRST_VALUE(amount) OVER (PARTITION BY region ORDER BY sale_date DESC, id DESC) AS last_via_first
FROM sales
ORDER BY id;
```

```
+----+--------+------------+--------+----------+------------+---------+----------------+
| id | region | sale_date  | amount | first_ok | last_wrong | last_ok | last_via_first |
+----+--------+------------+--------+----------+------------+---------+----------------+
|  1 | East   | 2024-01-01 |    100 |      100 |        100 |     300 |            300 |
|  2 | East   | 2024-01-02 |    200 |      100 |        200 |     300 |            300 |
|  3 | East   | 2024-01-03 |    150 |      100 |        150 |     300 |            300 |
|  4 | East   | 2024-01-03 |     50 |      100 |         50 |     300 |            300 |
|  5 | East   | 2024-01-04 |    300 |      100 |        300 |     300 |            300 |
|  6 | West   | 2024-01-01 |     80 |       80 |         80 |     100 |            100 |
|  7 | West   | 2024-01-02 |    120 |       80 |        120 |     100 |            100 |
|  8 | West   | 2024-01-03 |    200 |       80 |        200 |     100 |            100 |
|  9 | West   | 2024-01-04 |    100 |       80 |        100 |     100 |            100 |
+----+--------+------------+--------+----------+------------+---------+----------------+
```

`first_ok` works with the default frame because the frame always *starts* at the
partition's first row. `last_wrong` just echoes the current row, because the frame
always *ends* at the current row. There are two equally correct fixes:

- `last_ok` keeps `LAST_VALUE` and widens the frame to the whole partition.
- `last_via_first` reverses the sort (`ORDER BY sale_date DESC, id DESC`) and uses
  `FIRST_VALUE` — now the "first" row of the frame *is* the last sale. This needs no
  frame clause, which is why it is the more common idiom; the tiebreaker must be
  reversed too so both orderings pick the same row.

Note the outer `ORDER BY id`: without it MySQL is free to return rows in whatever order
the last window it evaluated left them in (here, the `DESC` one). Window functions
never define output order — only an outer `ORDER BY` does.

### 5f. `RANGE` with a value offset — when a row-count window is wrong

`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means "the 2 previous **physical rows**" —
not "the last 2 days". If the data has gaps (a day with no activity), `ROWS` quietly
reaches further back in time than intended, because it just counts rows, not calendar
distance. `RANGE` with a numeric/`INTERVAL` offset asks the question in terms of the
`ORDER BY` *value* itself, so it stays correct regardless of gaps — use it whenever the
window is supposed to mean "the last N units of the order-by value," not "the last N
rows."

```sql
WITH daily AS (
    SELECT CAST('2024-01-01' AS DATE) AS d, 100 AS amount UNION ALL
    SELECT CAST('2024-01-02' AS DATE), 200 UNION ALL
    SELECT CAST('2024-01-04' AS DATE), 150 UNION ALL   -- gap: no sales on 01-03
    SELECT CAST('2024-01-05' AS DATE), 300
)
SELECT d, amount,
       SUM(amount) OVER (
           ORDER BY d
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rows_3,
       SUM(amount) OVER (
           ORDER BY d
           RANGE BETWEEN INTERVAL 2 DAY PRECEDING AND CURRENT ROW
       ) AS range_2days
FROM daily;
```

```
+------------+--------+--------+-------------+
| d          | amount | rows_3 | range_2days |
+------------+--------+--------+-------------+
| 2024-01-01 |    100 |    100 |         100 |
| 2024-01-02 |    200 |    300 |         300 |
| 2024-01-04 |    150 |    450 |         350 |
| 2024-01-05 |    300 |    650 |         450 |
+------------+--------+--------+-------------+
```

On `2024-01-04`, `rows_3` grabs the 2 preceding *rows* — `01-01` and `01-02` — which
together span 3 calendar days, not 2. `range_2days` instead looks at the value of `d`
and correctly keeps only rows where `d` is within 2 days of `01-04`, i.e. `01-02` and
`01-04` (`01-03` doesn't exist, so it contributes nothing) — giving a true "trailing
2-day" sum. This is also why `RANGE` with a numeric/interval bound only allows a single
`ORDER BY` column: the bound is computed by adding/subtracting the offset from that
column's value, which is ambiguous with more than one sort key.

## Step 6: `LAG`/`LEAD` — offset functions, not frame functions

`LAG`/`LEAD` look like close cousins of `FIRST_VALUE`/`LAST_VALUE`, but they belong to
a different family: they only use `PARTITION BY`/`ORDER BY` and completely ignore any
`ROWS BETWEEN` clause. Adding a frame to a `LAG` call changes nothing — there is no
frame-default trap to fix here, unlike Step 5e.

That said, `LAG`/`LEAD` have their own gap: MySQL has no `IGNORE NULLS` option (some
engines — Snowflake, BigQuery, Oracle — do), so `LAG` always returns whatever sits in
the *literal* previous row, `NULL` included. That makes "carry forward the last known
value" — filling gaps with the most recent non-`NULL` value, a very common reporting
need — impossible with `LAG` alone.

The fix is the **running-max-of-a-group-id** trick: build a group id that only
advances on non-`NULL` rows, then let `MAX` (which ignores `NULL`) pull that group's
one real value across every row in it.

```sql
WITH src AS (
    SELECT 1 AS id, 'OPEN' AS status UNION ALL
    SELECT 2, NULL UNION ALL
    SELECT 3, NULL UNION ALL
    SELECT 4, 'CLOSED' UNION ALL
    SELECT 5, NULL UNION ALL
    SELECT 6, 'OPEN' UNION ALL
    SELECT 7, NULL
),
grouped AS (
    SELECT
        id,
        status,
        COUNT(status) OVER (ORDER BY id) AS grp
    FROM src
)
SELECT
    id,
    status,
    grp,
    MAX(status) OVER (PARTITION BY grp) AS status_filled,
    LAG(status) OVER (ORDER BY id)      AS plain_lag
FROM grouped
ORDER BY id;
```

```
+----+--------+-----+----------------+-----------+
| id | status | grp | status_filled  | plain_lag |
+----+--------+-----+----------------+-----------+
|  1 | OPEN   |   1 | OPEN           | NULL      |
|  2 | NULL   |   1 | OPEN           | OPEN      |
|  3 | NULL   |   1 | OPEN           | NULL      |
|  4 | CLOSED |   2 | CLOSED         | NULL      |
|  5 | NULL   |   2 | CLOSED         | CLOSED    |
|  6 | OPEN   |   3 | OPEN           | NULL      |
|  7 | NULL   |   3 | OPEN           | OPEN      |
+----+--------+-----+----------------+-----------+
```

`COUNT(status) OVER (ORDER BY id)` is a running count of *non-`NULL`* values seen so
far — `COUNT` skips `NULL`s, so it only ticks up on a real value and holds steady
across every `NULL` that follows, which is exactly what carves the rows into groups:
each group is one real value plus the run of `NULL`s immediately after it. Because
`MAX` also ignores `NULL`, `MAX(status) OVER (PARTITION BY grp)` reduces each group
down to its one non-`NULL` value and broadcasts it to every row in the group — no
`ORDER BY` needed inside that `OVER()`, since every row in a group is meant to land on
the same answer.

`plain_lag` shows why a plain `LAG` can't do this job: at row 3 it dutifully returns
row 2's value, which is `NULL` — it looks back exactly one physical row, it does not
"keep looking back until it finds something." `status_filled` is the general-purpose
answer whenever a `LAG`-family question turns out to actually be "what was the last
*known* value," not "what was the previous row."

## Putting it together

Reading a window function call from the inside out:

```sql
SUM(amount) OVER (                       -- 1. what to compute
    PARTITION BY region                  -- 3. restart per region
    ORDER BY sale_date, id               -- 4. walk the rows in this order
    ROWS BETWEEN 2 PRECEDING             -- 5. ...and for each row, look at
             AND CURRENT ROW             --    itself plus the two before it
)
```

| Clause present                      | Frame the function sees                         | Typical result        |
|-------------------------------------|-------------------------------------------------|-----------------------|
| `OVER ()`                           | entire result set                               | grand total           |
| `OVER (PARTITION BY g)`             | entire partition                                | group total           |
| `OVER (PARTITION BY g ORDER BY o)`  | partition start → current row **and its peers** | running total (ties lumped) |
| `... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | partition start → current row, row by row | running total |
| `... ROWS BETWEEN n PRECEDING AND CURRENT ROW` | last n+1 rows                        | moving average        |
| `... ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | entire partition (ordered) | `LAST_VALUE` done right |

Two rules of thumb that avoid most window-function bugs:

1. If `ORDER BY` can produce ties, add a unique tiebreaker column.
2. If you write `ORDER BY` and care about *which rows* are aggregated, write the
   `ROWS BETWEEN` clause explicitly rather than relying on the `RANGE` default.

## Further reading

- [MySQL — Window Function Concepts and Syntax](https://dev.mysql.com/doc/refman/8.0/en/window-functions-usage.html)
- [MySQL — Window Function Frame Specification](https://dev.mysql.com/doc/refman/8.0/en/window-functions-frames.html)

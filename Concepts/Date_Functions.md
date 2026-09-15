# Date & Time Functions in MySQL

MySQL's date functions fall into four jobs: **pulling a part out of a date**
(`DAYOFWEEK`, `DAYNAME`, ...), **shifting a date** (`ADDDATE`, `DATEDIFF`, ...),
**finding a boundary** (`LAST_DAY`, ...), and **formatting** (`DATE_FORMAT`).
This tutorial walks through each job against a small `orders` table, then closes
with two recursive-CTE tricks — generating a calendar row-by-row is one of the
most useful patterns in interview SQL (gap-filling, missing dates, "every day
this week" style questions).

Load the data with:

```bash
make setup Date_Functions.md
```

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id         INT PRIMARY KEY,
    customer   VARCHAR(10),
    order_date DATE,
    amount     INT
);

INSERT INTO orders (id, customer, order_date, amount) VALUES
(1, 'Ann',   '2026-09-01', 120),
(2, 'Ben',   '2026-09-03',  80),
(3, 'Ann',   '2026-09-08', 200),
(4, 'Cara',  '2026-09-10',  50),
(5, 'Ben',   '2026-09-14', 175),
(6, 'Ann',   '2026-09-21',  90),
(7, 'Cara',  '2026-09-30', 300);
```

`2026-09-01` is a Tuesday, so the dates above deliberately land on different
weekdays and straddle the start/end of the month — that's what makes
`DAYOFWEEK`, `LAST_DAY`, and the boundary tricks below show something other
than the same value repeated.

## Step 1: Pulling a part out of a date

```sql
SELECT
    order_date,
    DAYOFWEEK(order_date)  AS dow_num,     -- 1=Sunday ... 7=Saturday
    DAYNAME(order_date)    AS dow_name,
    DAYOFMONTH(order_date) AS day_of_month,
    DAYOFYEAR(order_date)  AS day_of_year,
    WEEK(order_date)       AS week_num,
    MONTHNAME(order_date)  AS month_name,
    QUARTER(order_date)    AS quarter,
    YEAR(order_date)       AS year
FROM orders
ORDER BY order_date;
```

```
+------------+---------+-----------+--------------+-------------+----------+------------+---------+------+
| order_date | dow_num | dow_name  | day_of_month | day_of_year | week_num | month_name | quarter | year |
+------------+---------+-----------+--------------+-------------+----------+------------+---------+------+
| 2026-09-01 |       3 | Tuesday   |            1 |         244 |       35 | September  |       3 | 2026 |
| 2026-09-03 |       5 | Thursday  |            3 |         246 |       35 | September  |       3 | 2026 |
| 2026-09-08 |       3 | Tuesday   |            8 |         251 |       36 | September  |       3 | 2026 |
| 2026-09-10 |       5 | Thursday  |           10 |         253 |       36 | September  |       3 | 2026 |
| 2026-09-14 |       2 | Monday    |           14 |         257 |       37 | September  |       3 | 2026 |
| 2026-09-21 |       2 | Monday    |           21 |         264 |       38 | September  |       3 | 2026 |
| 2026-09-30 |       4 | Wednesday |           30 |         273 |       39 | September  |       3 | 2026 |
+------------+---------+-----------+--------------+-------------+----------+------------+---------+------+
```

`DAYOFWEEK` is the one to watch: it's **1-indexed starting at Sunday**, which
trips people up coming from languages where Monday is day 0 or day 1. `WEEKDAY`
is the ISO-flavored alternative — 0=Monday ... 6=Sunday:

```sql
SELECT order_date, DAYOFWEEK(order_date) AS dayofweek, WEEKDAY(order_date) AS weekday
FROM orders
WHERE order_date = '2026-09-01';
```

```
+------------+-----------+---------+
| order_date | dayofweek | weekday |
+------------+-----------+---------+
| 2026-09-01 |         3 |       1 |
+------------+-----------+---------+
```

A common use of these: filter to weekend orders with `CASE`, since `IF()`
reads less clearly once conditions stack up:

```sql
SELECT
    order_date,
    CASE
        WHEN DAYOFWEEK(order_date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type
FROM orders
ORDER BY order_date;
```

```
+------------+----------+
| order_date | day_type |
+------------+----------+
| 2026-09-01 | Weekday  |
| 2026-09-03 | Weekday  |
| 2026-09-08 | Weekday  |
| 2026-09-10 | Weekday  |
| 2026-09-14 | Weekday  |
| 2026-09-21 | Weekday  |
| 2026-09-30 | Weekday  |
+------------+----------+
```

## Step 2: Shifting a date — `SUBDATE`, `ADDDATE`, `INTERVAL`

`ADDDATE`/`SUBDATE` move a date by an `INTERVAL`, same as `DATE_ADD`/
`DATE_SUB` — they're synonyms in that form. The interval unit (`DAY`, `WEEK`,
`MONTH`, `YEAR`, ...) tells MySQL how to count.

```sql
SELECT
    order_date,
    ADDDATE(order_date, INTERVAL 7 DAY)   AS plus_1_week,
    SUBDATE(order_date, INTERVAL 1 MONTH) AS minus_1_month,
    order_date + INTERVAL 1 YEAR          AS plus_1_year   -- same as ADDDATE
FROM orders
WHERE customer = 'Ann'
ORDER BY order_date;
```

```
+------------+-------------+---------------+-------------+
| order_date | plus_1_week | minus_1_month | plus_1_year |
+------------+-------------+---------------+-------------+
| 2026-09-01 | 2026-09-08  | 2026-08-01    | 2027-09-01  |
| 2026-09-08 | 2026-09-15  | 2026-08-08    | 2027-09-08  |
| 2026-09-21 | 2026-09-28  | 2026-08-21    | 2027-09-21  |
+------------+-------------+---------------+-------------+
```

`DATEDIFF` gives whole days between two dates; `TIMESTAMPDIFF` lets you pick
the unit (days, months, years, ...) and takes `(unit, start, end)` — note the
argument order is start-then-end, the opposite of subtraction order:

```sql
SELECT
    o1.customer,
    o1.order_date AS first_order,
    o2.order_date AS second_order,
    DATEDIFF(o2.order_date, o1.order_date)             AS days_between,
    TIMESTAMPDIFF(MONTH, o1.order_date, o2.order_date) AS months_between
FROM orders o1
JOIN orders o2
    ON o1.customer = o2.customer AND o1.id < o2.id
WHERE o1.customer = 'Ann';
```

```
+----------+-------------+--------------+--------------+----------------+
| customer | first_order | second_order | days_between | months_between |
+----------+-------------+--------------+--------------+----------------+
| Ann      | 2026-09-01  | 2026-09-08   |            7 |              0 |
| Ann      | 2026-09-01  | 2026-09-21   |           20 |              0 |
| Ann      | 2026-09-08  | 2026-09-21   |           13 |              0 |
+----------+-------------+--------------+--------------+----------------+
```

## Step 3: Finding a boundary — `LAST_DAY` and the first-of-month trick

`LAST_DAY` returns the last calendar day of a date's month — handy since
months don't all have the same length and there's no `FIRST_DAY`:

```sql
SELECT
    order_date,
    DATE_FORMAT(order_date, '%Y-%m-01') AS first_of_month,
    LAST_DAY(order_date)                AS last_of_month
FROM orders
WHERE customer = 'Cara';
```

```
+------------+----------------+---------------+
| order_date | first_of_month | last_of_month |
+------------+----------------+---------------+
| 2026-09-10 | 2026-09-01     | 2026-09-30    |
| 2026-09-30 | 2026-09-01     | 2026-09-30    |
+------------+----------------+---------------+
```

The same "first of month" can also be written `SUBDATE(order_date, INTERVAL
DAYOFMONTH(order_date) - 1 DAY)` — both are common in solutions, `DATE_FORMAT`
is usually the more readable one.

### `SUBDATE`/`ADDDATE` vs `DATE_SUB`/`DATE_ADD`

`SUBDATE`/`ADDDATE` are synonyms for `DATE_SUB`/`DATE_ADD` — but only when
called with an `INTERVAL` expression. They also accept a second form,
`SUBDATE(date, days)`/`ADDDATE(date, days)`, where `days` is a plain integer
(implicitly `DAY`s). `DATE_SUB`/`DATE_ADD` have no such shorthand — passing a
bare integer instead of `INTERVAL n DAY` is a syntax error:

```sql
SELECT SUBDATE('2026-09-15', 7);   -- 2026-09-08, OK
SELECT DATE_SUB('2026-09-15', 7);  -- ERROR 1064: syntax error
```

Prefer `SUBDATE`/`ADDDATE` over `DATE_SUB`/`DATE_ADD` in this repo's
solutions — the plain-integer form reads more compactly for the common "shift
by N days" case, and `SUBDATE`/`ADDDATE` still accept `INTERVAL` when a
different unit (`MONTH`, `YEAR`, ...) is needed, so there's no case where
`DATE_SUB`/`DATE_ADD` can do something they can't.

## Step 4: Formatting — `DATE_FORMAT` and `STR_TO_DATE`

`DATE_FORMAT` turns a `DATE`/`DATETIME` into a string using `%`-codes
(`%Y` year, `%m` zero-padded month, `%d` zero-padded day, `%M` full month
name, `%W` full weekday name). `STR_TO_DATE` is the inverse — parsing a string
into a date using the same codes.

```sql
SELECT
    order_date,
    DATE_FORMAT(order_date, '%W, %M %e, %Y') AS pretty,
    DATE_FORMAT(order_date, '%Y-%m')         AS ym
FROM orders
ORDER BY order_date
LIMIT 3;
```

```
+-------------+-----------------------------+---------+
| order_date  | pretty                      | ym      |
+-------------+-----------------------------+---------+
| 2026-09-01  | Tuesday, September 1, 2026  | 2026-09 |
| 2026-09-03  | Thursday, September 3, 2026 | 2026-09 |
| 2026-09-08  | Tuesday, September 8, 2026  | 2026-09 |
+-------------+-----------------------------+---------+
```

```sql
SELECT STR_TO_DATE('08/14/2026', '%m/%d/%Y') AS parsed;
```

```
+------------+
| parsed     |
+------------+
| 2026-08-14 |
+------------+
```

`ym` from `DATE_FORMAT(..., '%Y-%m')` is the standard trick for "group orders
by month" — group by the formatted string (or an equivalent
`DATE_FORMAT(order_date, '%Y-%m-01')` if you want a real `DATE` back instead
of a string). Watch the alias name though: `year_month` looks like an
ordinary identifier but is actually reserved (it's the `INTERVAL ...
YEAR_MONTH` unit), so `AS year_month` throws a syntax error unless you quote
it as `` `year_month` ``. When a plain-looking alias fails to parse, a
reserved word is the first thing to suspect.

## Step 5: Recursive CTE tricks

A recursive CTE builds rows one at a time: an **anchor** query produces the
starting row(s), then the **recursive** part repeatedly joins against the CTE
itself, adding one new row per pass, until its `WHERE` clause stops matching.
For dates, that means you can generate a calendar — a sequence of consecutive
dates — without a pre-existing table of them.

### 5a. Generate all seven day names for a week

Starting from any date, add a day at a time and stop after 7 rows:

```sql
WITH RECURSIVE days AS (
    SELECT DATE('2026-09-14') AS dt, 1 AS n

    UNION ALL

    SELECT ADDDATE(dt, INTERVAL 1 DAY), n + 1
    FROM days
    WHERE n < 7
)
SELECT
    dt,
    DAYNAME(dt) AS day_name
FROM days;
```

```
+------------+-----------+
| dt         | day_name  |
+------------+-----------+
| 2026-09-14 | Monday    |
| 2026-09-15 | Tuesday   |
| 2026-09-16 | Wednesday |
| 2026-09-17 | Thursday  |
| 2026-09-18 | Friday    |
| 2026-09-19 | Saturday  |
| 2026-09-20 | Sunday    |
+------------+-----------+
```

The `n` counter is what makes this safe: without a `WHERE n < 7` (or an
equivalent bound on `dt`), the recursion never terminates. MySQL's default
`cte_max_recursion_depth` (1000) is a safety net, not a substitute for a real
stop condition.

### 5b. Find days in September with **no** orders

This is the pattern the anchor trick is really for: generate every date in a
range, then `LEFT JOIN` real data onto it to expose the gaps — a much cleaner
approach than eyeballing which dates are "missing" from the `orders` table.

```sql
WITH RECURSIVE calendar AS (
    SELECT DATE('2026-09-01') AS dt

    UNION ALL

    SELECT ADDDATE(dt, INTERVAL 1 DAY)
    FROM calendar
    WHERE dt < '2026-09-30'
)
SELECT
    c.dt,
    DAYNAME(c.dt) AS day_name
FROM calendar c
LEFT JOIN orders o ON o.order_date = c.dt
WHERE o.id IS NULL
ORDER BY c.dt;
```

```
+------------+-----------+
| dt         | day_name  |
+------------+-----------+
| 2026-09-02 | Wednesday |
| 2026-09-04 | Friday    |
| 2026-09-05 | Saturday  |
| 2026-09-06 | Sunday    |
| 2026-09-07 | Monday    |
| 2026-09-09 | Wednesday |
...
+------------+-----------+
```

Bounding the recursion on `dt < '2026-09-30'` (rather than a row counter like
`n`) works just as well here — anchor the stop condition on whichever value
naturally has a known endpoint.

## Further reading

- [MySQL date/time function reference](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html)
- [MySQL `WITH` (Common Table Expressions) reference](https://dev.mysql.com/doc/refman/8.4/en/with.html) — covers `RECURSIVE` and `cte_max_recursion_depth`
- [Window_Function_Anatomy.md](Window_Function_Anatomy.md) — this repo's companion tutorial on window functions

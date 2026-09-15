# 1321. Restaurant Growth - Solutions

## Solution 1: Daily totals, then a sliding window average

Multiple customers can visit on the same `visited_on`, so the first step is to
collapse `Customer` down to one row per day holding that day's total
`amount`. Once every day is represented exactly once, `AVG(total_amount)
OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` computes
the 7-day moving average directly — no need to sum and divide by 7 by hand,
since `AVG` already expresses "moving average" without a magic constant.

The window is only complete once at least 7 distinct days have been seen, so
dates before `ADDDATE(MIN(visited_on), 6)` (the earliest date with a full
7-day history behind it) are filtered out.

#### MySQL

```sql
WITH
    daily AS (
        SELECT visited_on, SUM(amount) AS total_amount
        FROM Customer
        GROUP BY visited_on
    )
SELECT visited_on, amount, average_amount
FROM (
    SELECT
        visited_on,
        SUM(total_amount) OVER (
            ORDER BY visited_on
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS amount,
        ROUND(AVG(total_amount) OVER (
            ORDER BY visited_on
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2) AS average_amount
    FROM daily
) AS t
WHERE visited_on >= ADDDATE((SELECT MIN(visited_on) FROM Customer), 6)
ORDER BY visited_on;
```

**Step by step:**

1. **`daily`** — groups `Customer` by `visited_on` so same-day visits are
   combined into a single per-day `total_amount`.
2. **Window functions** — `SUM(...)`/`AVG(...) OVER (... ROWS BETWEEN 6
   PRECEDING AND CURRENT ROW)` fold each day's total together with the six
   days before it into a running window sum and average.
3. **Filter** — `ADDDATE(MIN(visited_on), 6)` marks the first date with a
   full 7-day window behind it; earlier dates (whose window would be
   incomplete) are excluded.

## Solution 2: Daily totals with an explicit row-position filter

Equivalent to Solution 1, but instead of filtering on a computed date
threshold, `ROW_NUMBER() OVER (ORDER BY visited_on)` tags each distinct day
with its position in the sequence, and only rows numbered `7` or later (i.e.
the 7th day onward) have a full window behind them.

#### MySQL

```sql
WITH
    daily AS (
        SELECT visited_on, SUM(amount) AS amount
        FROM Customer
        GROUP BY visited_on
    ),
    windowed AS (
        SELECT
            visited_on,
            SUM(amount) OVER (
                ORDER BY visited_on
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ) AS amount,
            ROW_NUMBER() OVER (ORDER BY visited_on) AS rn
        FROM daily
    )
SELECT visited_on, amount, ROUND(amount / 7, 2) AS average_amount
FROM windowed
WHERE rn >= 7
ORDER BY visited_on;
```

**Step by step:**

1. **`daily`** — groups `Customer` by `visited_on` so same-day visits are
   combined into a single per-day `amount`.
2. **`windowed`** — the window sum accumulates each day's total plus the six
   days before it; `rn` numbers the distinct days in chronological order.
3. **Filter** — `rn >= 7` keeps only days whose window is a full 7 days
   (dropping the first six days, which don't have six prior days to draw on),
   and `ROUND(amount / 7, 2)` turns the window sum into the requested average.

## Solution 3: Self join on a bounded date difference

Without window functions, the same 7-day window can be built with a join:
pair every distinct date `a.visited_on` with the detail rows `b` whose
`visited_on` falls within 6 days before it (`DATEDIFF(a.visited_on,
b.visited_on) BETWEEN 0 AND 6`), then sum `b.amount` per `a.visited_on`.

As with Solutions 1 and 2, only dates that are at least 6 days after the
earliest `visited_on` have a full window, so those are filtered out up front
rather than relying on the join to short-circuit. `ADDDATE(date, 6)` is used
instead of plain `date + 6` — MySQL evaluates `date + 6` as numeric addition
on the date's `YYYYMMDD` representation, which silently produces the wrong
date once the day-of-month is within 6 of rolling into the next month (e.g.
`'2019-01-28' + 6` yields the nonsensical `20190134`, not `2019-02-03`).

#### MySQL

```sql
SELECT
    a.visited_on,
    SUM(b.amount) AS amount,
    ROUND(SUM(b.amount) / 7, 2) AS average_amount
FROM (SELECT DISTINCT visited_on FROM Customer) AS a
JOIN Customer AS b ON DATEDIFF(a.visited_on, b.visited_on) BETWEEN 0 AND 6
WHERE a.visited_on >= ADDDATE((SELECT MIN(visited_on) FROM Customer), 6)
GROUP BY a.visited_on
ORDER BY a.visited_on;
```

**Step by step:**

1. **`a`** — the distinct set of dates the moving average is computed for.
2. **Join condition** — `DATEDIFF(a.visited_on, b.visited_on) BETWEEN 0 AND 6`
   pulls in every detail row from the 7-day window ending on `a.visited_on`
   (itself included, at a difference of `0`).
3. **Filter** — `a.visited_on >= ADDDATE(MIN(visited_on), 6)` drops dates that
   don't yet have a full 6 days of history behind them.
4. **Aggregate** — grouping by `a.visited_on` sums the matched `amount`s into
   the window total, and dividing by 7 gives `average_amount`.

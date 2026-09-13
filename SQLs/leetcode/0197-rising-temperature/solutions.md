# 197. Rising Temperature - Solutions

## Solution 1: Self-join on `DATEDIFF`

Join `Weather` to itself on `DATEDIFF(w1.recordDate, w2.recordDate) = 1`, i.e.
`w2` is exactly one calendar day before `w1`. The join condition itself
guarantees the two rows are actually consecutive calendar dates (not just
consecutive rows), so a plain `>` on `temperature` after that is enough to
confirm a rise.

#### MySQL

```sql
SELECT w1.id
FROM
    Weather AS w1
    JOIN Weather AS w2
        ON DATEDIFF(w1.recordDate, w2.recordDate) = 1 AND w1.temperature > w2.temperature;
```

## Solution 2: `LAG` over `recordDate`

`LAG` (ordered by `recordDate`) pulls each row's previous day's temperature
and date into the same row as `prev_temperature`/`prev_Date`. Unlike
Solution 1's join, `LAG` only knows about row order, not the actual gap
between dates — if a day is missing from the table, the row before it in
`recordDate` order still gets treated as its "previous" row. The explicit
`DATEDIFF(recordDate, prev_Date) = 1` check is what rules that out, so a
missing day correctly breaks the chain instead of being silently skipped
over.

#### MySQL

```sql
WITH T AS (
    SELECT
        id,
        recordDate,
        temperature,
        LAG(temperature, 1) OVER (ORDER BY recordDate) AS prev_temperature,
        LAG(recordDate, 1)  OVER (ORDER BY recordDate) AS prev_Date
    FROM Weather
)
SELECT id
FROM T
WHERE temperature > prev_temperature
  AND prev_temperature IS NOT NULL
  AND prev_Date IS NOT NULL
  AND DATEDIFF(recordDate, prev_Date) = 1;
```

The `prev_temperature IS NOT NULL`/`prev_Date IS NOT NULL` checks guard the
first row in `recordDate` order, whose `LAG` values are `NULL` — without
them, `temperature > NULL` is simply unknown (not true), so those checks are
technically redundant here, but they make the "no previous day" case explicit
rather than relying on SQL's `NULL`-comparison semantics.

<!-- problem:start -->

# [571. Find Median Given Frequency of Numbers 🔒](https://leetcode.com/problems/find-median-given-frequency-of-numbers)

## Description

<!-- description:start -->

<p>Table: <code>Numbers</code></p>

<pre>
+-------------+------+
| Column Name | Type |
+-------------+------+
| num         | int  |
| frequency   | int  |
+-------------+------+
</pre>

<p>num is the primary key (column with unique values) for this table.</p>

<p>Each row of this table shows the number <code>num</code> and how many times it appears in an array (its <code>frequency</code>). The array is the <em>decompressed</em> form of this frequency table.</p>

<p>Write a solution to report the <strong>median</strong> of the numbers in the decompressed array. The median of an array of even length is the average of the two middle values. Round the answer to <strong>one decimal place</strong>.</p>

<p>The result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
Numbers table:
+-----+-----------+
| num | frequency |
+-----+-----------+
| 0   | 7         |
| 1   | 1         |
| 2   | 3         |
| 3   | 1         |
+-----+-----------+
<strong>Output:</strong>
+--------+
| median |
+--------+
| 0.0    |
+--------+
<strong>Explanation:</strong>
The decompressed array is [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3].
It has 12 elements, so the median is the average of the two middle values, both 0, giving 0.0.
</pre>

<!-- description:end -->

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Numbers;

CREATE TABLE Numbers (
    num       INT PRIMARY KEY,
    frequency INT
);

INSERT INTO Numbers (num, frequency) VALUES
(0, 7),
(1, 1),
(2, 3),
(3, 1);
```

## Setup2

An odd-length dataset whose decompressed array is **not** already sorted by scan order.
It trips up the two classic mistakes at once: relying on implicit row order (no `ORDER BY`
in `ROW_NUMBER()`) and using a `CASE`/division that breaks for odd lengths.

Decompressed sorted array: `[0, 5, 100]` — total = 3 (odd), correct median `5.0`.

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Numbers;

CREATE TABLE Numbers (
    num       INT PRIMARY KEY,
    frequency INT
);

INSERT INTO Numbers (num, frequency) VALUES
(0, 1),
(5, 1),
(100, 1);
```

## Solutions

<!-- solution:start -->

### Solution 1: Decompress with a recursive CTE, then take the middle position(s)

Rebuild the actual array and read off its middle, just like you would by hand.

1. A recursive CTE generates the integers `1 … MAX(frequency)`. Joining `Numbers` to it on `frequency >= rn` emits each `num` exactly `frequency` times — the decompressed array.
2. `ROW_NUMBER() OVER (ORDER BY num)` numbers those copies in **sorted** order (the explicit `ORDER BY` is essential — a table has no inherent order to rely on), and `COUNT(*) OVER ()` gives the total length `total_num`.
3. The middle position(s) are exactly the rows with `total_num/2 <= rnk <= total_num/2 + 1`. Because MySQL's `/` is decimal division, this single predicate handles both parities: for an **even** length the endpoints land on whole numbers (`.0`), selecting the two middle rows; for an **odd** length they land on `.5`, selecting the one middle row. Averaging the selected `num`s and rounding gives the median.

<!-- tabs:start -->

#### MySQL

```sql
WITH RECURSIVE cte AS (
    SELECT 1 AS rn
    UNION ALL
    SELECT rn + 1 FROM cte WHERE rn < (SELECT MAX(frequency) FROM Numbers)
),
cte2 AS (
    SELECT
        n.num,
        ROW_NUMBER() OVER (ORDER BY n.num) AS rnk,
        COUNT(*)     OVER ()               AS total_num
    FROM Numbers AS n
    JOIN cte AS c ON n.frequency >= c.rn
)
SELECT ROUND(AVG(num), 1) AS median
FROM cte2
WHERE rnk >= total_num / 2
  AND rnk <= total_num / 2 + 1;
```

<!-- tabs:end -->

> For the example the decompressed sorted array is `[0,0,0,0,0,0,0,1,2,2,2,3]` (length 12). The predicate keeps `rnk` 6 and 7 — both `0` — so the median is `0.0`. This approach materializes the whole array (Σ frequency rows), so Solution 2 is cheaper when frequencies are large.

### Solution 2: Two-directional running totals

**Intuition:** a number can be the median only if there are enough elements on **both** sides of it. So count, for each value, how much of the array lies on each side — without decompressing.

Let `s` be the total number of elements. For each `num`:

- `rk1` = cumulative frequency from the left = number of elements `<= num`,
- `rk2` = cumulative frequency from the right = number of elements `>= num`.

Then the two conditions

```
rk1 >= s / 2   -- enough elements up to and including this number
rk2 >= s / 2   -- enough elements from this number onward
```

each say "this value reaches at least the halfway mark from its side." Their **intersection** pins down the value(s) that contain the middle of the sorted array. For even `s` two adjacent values satisfy both (the two middle blocks); for odd `s` exactly one does. Averaging the matching `num`s therefore yields the median for both parities.

<!-- tabs:start -->

#### MySQL

```sql
WITH t AS (
    SELECT
        num,
        SUM(frequency) OVER (ORDER BY num ASC)  AS rk1,
        SUM(frequency) OVER (ORDER BY num DESC) AS rk2,
        SUM(frequency) OVER ()                  AS s
    FROM Numbers
)
SELECT ROUND(AVG(num), 1) AS median
FROM t
WHERE rk1 >= s / 2 AND rk2 >= s / 2;
```

<!-- tabs:end -->

<!-- solution:end -->

<!-- problem:end -->

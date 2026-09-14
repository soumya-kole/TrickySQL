# Paired Products (Frequently Bought Together)

Say `transactions` holds over a billion rows of line items purchased by users. Find
which pairs of products are most often bought together in the same transaction — e.g.
wine and a bottle opener, chips and beer.

## Description

<p>Table: <code>transactions</code></p>

<pre>
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| transaction_id | int      |
| user_id        | int      |
| created_at     | datetime |
| product_id     | int      |
| quantity       | int      |
+----------------+----------+
Each row is one line item: quantity units of product_id purchased by user_id as part
of transaction_id. A transaction can have multiple line items (one row each), all
sharing the same transaction_id.
</pre>

<p>Table: <code>products</code></p>

<pre>
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| price       | decimal |
+-------------+---------+
id is the primary key for this table.
</pre>

<p>Find the top 3 pairs of distinct products most often purchased together in the same
transaction. Dedupe each unordered pair by keeping only the combination where the first
product's <code>id</code> is smaller than the second's; count the transactions
containing that pair as <code>pair_cnt</code>, and sum the smaller-<code>id</code>
product's quantity across those transactions as <code>total_qty</code>. Return the
pair's two product names sorted alphabetically as <code>p1</code> and <code>p2</code>
(independent of which product's <code>id</code> was smaller). Order the result by
<code>pair_cnt</code> descending, then <code>total_qty</code> descending, then
<code>p1</code>, then <code>p2</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
products table:
+----+---------------+-------+
| id | name          | price |
+----+---------------+-------+
| 1  | Wine          | 15.00 |
| 2  | Bottle Opener | 5.00  |
| 3  | Chips         | 2.50  |
| 4  | Beer          | 8.00  |
| 5  | Soda          | 3.00  |
+----+---------------+-------+
transactions table:
+----------------+---------+---------------------+------------+----------+
| transaction_id | user_id | created_at          | product_id | quantity |
+----------------+---------+---------------------+------------+----------+
| 1              | 101     | 2024-10-01 12:00:00 | 1          | 1        |
| 1              | 101     | 2024-10-01 12:00:00 | 2          | 1        |
| 1              | 101     | 2024-10-01 12:00:00 | 4          | 1        |
| 6              | 101     | 2024-10-01 13:00:00 | 1          | 1        |
| 6              | 101     | 2024-10-01 13:00:00 | 2          | 1        |
| 2              | 102     | 2024-10-01 12:30:00 | 3          | 2        |
| 2              | 102     | 2024-10-01 12:30:00 | 4          | 1        |
| 3              | 103     | 2024-10-01 13:00:00 | 1          | 1        |
| 3              | 103     | 2024-10-01 13:00:00 | 4          | 1        |
| 4              | 104     | 2024-10-01 14:00:00 | 3          | 3        |
| 4              | 104     | 2024-10-01 14:00:00 | 2          | 1        |
| 5              | 105     | 2024-10-01 14:30:00 | 5          | 2        |
| 5              | 105     | 2024-10-01 14:30:00 | 1          | 1        |
+----------------+---------+---------------------+------------+----------+
<strong>Output:</strong>
+----------------+------+----------+-----------+
| p1             | p2   | pair_cnt | total_qty |
+----------------+------+----------+-----------+
| Beer           | Wine | 2        | 2         |
| Bottle Opener  | Wine | 2        | 2         |
| Beer           | Chips| 1        | 2         |
+----------------+------+----------+-----------+
<strong>Explanation:</strong>
Wine (id 1) and Beer (id 4) appear together in transactions 1 and 3 — pair_cnt 2, and
since id 1 < id 4, total_qty sums Wine's quantity (1 + 1 = 2). Bottle Opener (id 2) and
Wine (id 1) appear together in transactions 1 and 6 — also pair_cnt 2, total_qty 2
(Wine's quantity again, since id 1 < id 2) — tied with the first pair, so it sorts
second by product name (Beer < Bottle Opener alphabetically). Beer (id 4) and Chips
(id 3) appear together only in transaction 2, but Chips' quantity there is 2 and id 3
< id 4, so total_qty is 2 despite pair_cnt being only 1 — enough to edge out the other
single-transaction pairs (Bottle Opener+Chips, Bottle Opener+Beer, Wine+Soda), which
all have total_qty 1.
</pre>

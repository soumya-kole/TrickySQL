# Explode Implementation (SQL-only, no procedure)

Pure-SQL equivalent of `EXPLODE()` (Hive/Spark) or `UNNEST()`: split a comma-separated
string column into one row per value, using only a recursive CTE — no stored procedure,
UDF, or `JSON_TABLE`.

## Description

<p>Table: <code>explode_table</code></p>

<pre>
+-------------+-------------+
| Column Name | Type        |
+-------------+-------------+
| id          | int         |
| csv_column  | varchar     |
+-------------+-------------+
id is the primary key for this table.
csv_column holds a comma-separated list of values (possibly a single value with no comma).
</pre>

<p>For every row, split <code>csv_column</code> on <code>,</code> and return one output row per
value, keeping the original <code>id</code>. Order the result by <code>id</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
explode_table table:
+----+---------------------+
| id | csv_column          |
+----+---------------------+
| 1  | apple                |
| 2  | dog,cat,horse        |
| 3  | one,two,three,four   |
+----+---------------------+
<strong>Output:</strong>
+----+--------+
| id | value  |
+----+--------+
| 1  | apple  |
| 2  | dog    |
| 2  | cat    |
| 2  | horse  |
| 3  | one    |
| 3  | two    |
| 3  | three  |
| 3  | four   |
+----+--------+
<strong>Explanation:</strong>
Row 1 has no comma, so it passes through unchanged. Rows 2 and 3 are split into one
output row per comma-separated value, preserving the original id.
</pre>

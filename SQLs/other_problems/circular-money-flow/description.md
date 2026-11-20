# Circular Money Flow

Source: [YouTube](https://www.youtube.com/watch?v=sHDTputXFfE&t=272s)

## Description

<p>Table: <code>transactions</code></p>

<pre>
+------------------+----------+
| Column Name      | Type     |
+------------------+----------+
| transaction_id   | int      |
| sender_id        | varchar  |
| receiver_id      | varchar  |
| amount           | int      |
| transaction_time | datetime |
+------------------+----------+
transaction_id is the primary key for this table.
Each row records a transfer of amount from sender_id to receiver_id at transaction_time.
</pre>

<p>Find all groups of users involved in a circular money flow where:</p>

<ol>
	<li>Money starts from User A.</li>
	<li>Passes through one or more intermediate users.</li>
	<li>Returns to User A.</li>
	<li>All transfers in the cycle occur within 1 hour.</li>
	<li>The transferred amount remains the same throughout the cycle.</li>
	<li>Each transfer happens after the previous one.</li>
	<li>Intermediate users may appear more than once, but the starting user appears only at
	the start and the end.</li>
</ol>

<p>Report every cycle, including shorter cycles contained within a longer one.</p>

<p>Return <code>cycle_id</code>, the <code>path</code> of users joined by <code>-></code>,
the <code>amount</code>, and the <code>cycle_length</code> (number of transfers in the
cycle).</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
transactions table:
+----------------+-----------+-------------+--------+---------------------+
| transaction_id | sender_id | receiver_id | amount | transaction_time    |
+----------------+-----------+-------------+--------+---------------------+
| 1              | 101       | 102         | 500    | 2025-01-01 09:00:00 |
| 2              | 102       | 103         | 500    | 2025-01-01 09:10:00 |
| 3              | 103       | 101         | 500    | 2025-01-01 09:20:00 |
| 4              | 201       | 202         | 1000   | 2025-01-01 10:00:00 |
| 5              | 202       | 203         | 1000   | 2025-01-01 10:05:00 |
| 6              | 203       | 204         | 1000   | 2025-01-01 10:10:00 |
+----------------+-----------+-------------+--------+---------------------+
<strong>Output:</strong>
+----------+--------------------+--------+--------------+
| cycle_id | path               | amount | cycle_length |
+----------+--------------------+--------+--------------+
| 1        | 101->102->103->101 | 500    | 3            |
+----------+--------------------+--------+--------------+
<strong>Explanation:</strong>
101 sends 500 to 102, 102 forwards 500 to 103, and 103 returns 500 to 101 — all within
20 minutes, with the same amount and each transfer after the previous one, so it forms a
cycle of length 3.
The 201 -> 202 -> 203 -> 204 chain never returns to 201, so it is not a cycle.
</pre>

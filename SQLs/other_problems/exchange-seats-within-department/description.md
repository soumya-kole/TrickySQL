# Exchange Seats (within Department)

Variant of LeetCode [626. Exchange Seats](https://leetcode.com/problems/exchange-seats/), with a twist: students are grouped by `dept`, and swaps must happen **within the same department** rather than across the whole table.

## Description

<p>Table: <code>Seat</code></p>

<pre>
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| dept        | varchar |
| id          | int     |
| student     | varchar |
+-------------+---------+
(dept, id) is the primary key for this table.
Each row shows a student's seat id within their department.
Ids are continuous per department, starting at 1.
</pre>

<p>Swap the seat id of each pair of adjacent students within the same <code>dept</code> (1 with 2, 3 with 4, and so on). If a department has an odd number of students, the last student's id stays unchanged.</p>

<p>Return the result ordered by <code>dept</code>, then <code>id</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
Seat table:
+------+----+---------+
| dept | id | student |
+------+----+---------+
| IT   | 1  | Abbot   |
| IT   | 2  | Doris   |
| IT   | 3  | Emerson |
| IT   | 4  | Green   |
| IT   | 5  | Jeames  |
| EC   | 1  | AA      |
| EC   | 2  | BB      |
| EC   | 3  | CC      |
| EC   | 4  | DD      |
+------+----+---------+
<strong>Output:</strong>
+------+----+---------+
| dept | id | student |
+------+----+---------+
| EC   | 1  | BB      |
| EC   | 2  | AA      |
| EC   | 3  | DD      |
| EC   | 4  | CC      |
| IT   | 1  | Doris   |
| IT   | 2  | Abbot   |
| IT   | 3  | Green   |
| IT   | 4  | Emerson |
| IT   | 5  | Jeames  |
+------+----+---------+
<strong>Explanation:</strong>
Within IT, (Abbot, Doris) swap, (Emerson, Green) swap, and Jeames (odd one out, last seat) keeps id 5.
Within EC, (AA, BB) swap and (CC, DD) swap.
</pre>

# Match Win/Loss Summary

Source: [ICC Tournament Points Table SQL Interview Question](https://www.youtube.com/watch?v=qyAgWL066Vo&list=PLBTZqjSKn0IeKBQDjLmzisazhqQy4iGkb)

## Description

<p>Table: <code>icc_world_cup</code></p>

<pre>
+-------------+-------------+
| Column Name | Type        |
+-------------+-------------+
| Team_1      | varchar(20) |
| Team_2      | varchar(20) |
| Winner      | varchar(20) |
+-------------+-------------+
Each row is one match played between Team_1 and Team_2, with Winner naming
which of the two won. There are no tied/drawn matches in this problem setup.
</pre>

<p>Write a SQL query to derive the aggregated points table showing the following metrics for every participating team:</p>

<ul>
	<li><code>team</code>: the team name.</li>
	<li><code>total_matches</code>: total number of matches the team played (either as <code>Team_1</code> or <code>Team_2</code>).</li>
	<li><code>no_of_win</code>: total number of matches the team won.</li>
	<li><code>no_of_loses</code>: total number of matches the team lost.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
icc_world_cup table:
+--------+--------+--------+
| Team_1 | Team_2 | Winner |
+--------+--------+--------+
| India  | SL     | India  |
| SL     | Aus    | Aus    |
| SA     | Eng    | Eng    |
| Eng    | NZ     | NZ     |
| Aus    | India  | India  |
+--------+--------+--------+
<strong>Output:</strong>
+-------+---------------+-----------+-------------+
| team  | total_matches | no_of_win | no_of_loses |
+-------+---------------+-----------+-------------+
| India | 2             | 2         | 0           |
| NZ    | 1             | 1         | 0           |
| Eng   | 2             | 1         | 1           |
| Aus   | 2             | 1         | 1           |
| SA    | 1             | 0         | 1           |
| SL    | 2             | 0         | 2           |
+-------+---------------+-----------+-------------+
<strong>Explanation:</strong>
India played 2 matches (vs SL, vs Aus) and won both. NZ played 1 match (vs Eng)
and won it. Eng and Aus each played 2 matches, winning 1 and losing 1. SA played
1 match (vs Eng) and lost it. SL played 2 matches (vs India, vs Aus) and lost both.
</pre>

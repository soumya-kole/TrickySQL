# [2010. The Number of Seniors and Juniors to Join the Company II](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company-ii)

## Description

<p>Table: <code>Candidates</code></p>

<pre>
+-------------+------+
| Column Name | Type |
+-------------+------+
| employee_id | int  |
| experience  | enum |
| salary      | int  |
+-------------+------+
employee_id is the primary key column for this table.
experience is an enum with one of the values ('Senior', 'Junior').
Each row of this table indicates the id of a candidate, their monthly salary, and their experience.
The salary of each candidate is guaranteed to be <strong>unique</strong>.</pre>

<p>&nbsp;</p>

<p>A company wants to hire new employees. The budget of the company for the salaries is <code>$70000</code>. The company's criteria for hiring are:</p>

<ol>
	<li>Keep hiring the senior with the smallest salary until you cannot hire any more seniors.</li>
	<li>Use the remaining budget to hire the junior with the smallest salary.</li>
	<li>Keep hiring the junior with the smallest salary until you cannot hire any more juniors.</li>
</ol>

<p>Write an SQL query to find the ids of seniors and juniors hired under the mentioned criteria.</p>

<p>Return the result table in <strong>any order</strong>.</p>

<p>The query result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
Candidates table:
+-------------+------------+--------+
| employee_id | experience | salary |
+-------------+------------+--------+
| 1           | Junior     | 10000  |
| 9           | Junior     | 15000  |
| 2           | Senior     | 20000  |
| 11          | Senior     | 16000  |
| 13          | Senior     | 50000  |
| 4           | Junior     | 40000  |
+-------------+------------+--------+
<strong>Output:</strong> 
+-------------+
| employee_id |
+-------------+
| 11          |
| 2           |
| 1           |
| 9           |
+-------------+
<strong>Explanation:</strong> 
We can hire 2 seniors with IDs (11, 2). Since the budget is $70000 and the sum of their salaries is $36000, we still have $34000 but they are not enough to hire the senior candidate with ID 13.
We can hire 2 juniors with IDs (1, 9). Since the remaining budget is $34000 and the sum of their salaries is $25000, we still have $9000 but they are not enough to hire the junior candidate with ID 4.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong>
Candidates table:
+-------------+------------+--------+
| employee_id | experience | salary |
+-------------+------------+--------+
| 1           | Junior     | 25000  |
| 9           | Junior     | 10000  |
| 2           | Senior     | 85000  |
| 11          | Senior     | 80000  |
| 13          | Senior     | 90000  |
| 4           | Junior     | 30000  |
+-------------+------------+--------+
<strong>Output:</strong> 
+-------------+
| employee_id |
+-------------+
| 9           |
| 1           |
| 4           |
+-------------+
<strong>Explanation:</strong> 
We cannot hire any seniors with the current budget as we need at least $80000 to hire one senior.
We can hire all three juniors with the remaining budget.
</pre>

<p><strong class="example">Example 3 (custom edge case):</strong></p>

<pre>
<strong>Input:</strong>
Candidates table:
+-------------+------------+--------+
| employee_id | experience | salary |
+-------------+------------+--------+
| 1           | Senior     | 30000  |
| 2           | Senior     | 40000  |
| 3           | Senior     | 50000  |
| 4           | Junior     | 5000   |
| 5           | Junior     | 3000   |
+-------------+------------+--------+
<strong>Output:</strong> 
+-------------+
| employee_id |
+-------------+
| 1           |
| 2           |
+-------------+
<strong>Explanation:</strong> 
We can hire 2 seniors with IDs (1, 2). Since the budget is $70000 and the sum of their salaries is exactly $70000, we have $0 remaining and cannot hire the senior candidate with ID 3.
With $0 remaining budget, we cannot hire any juniors, even though candidates 4 and 5 have small salaries.
This case exercises the boundary where the running salary total lands exactly on the budget, leaving $0 (not a negative number) for the next group.
</pre>

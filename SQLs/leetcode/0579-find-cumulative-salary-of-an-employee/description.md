# [579. Find Cumulative Salary of an Employee](https://leetcode.com/problems/find-cumulative-salary-of-an-employee)

## Description

<p>Table: <code>Employee</code></p>

<pre>
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| month       | int  |
| salary      | int  |
+-------------+------+
(id, month) is the primary key (combination of columns with unique values) for this table.
Each row denotes the salary of an employee in a given month.
The table does not contain data for all months of each employee.
</pre>

<p>&nbsp;</p>

<p>Write a solution to calculate the salary summary for each employee.</p>

<p>The salary summary for a given employee can be calculated as follows:</p>

<ul>
	<li>For each month that the employee worked, sum up the salaries in that month and the previous two months. This is their <strong>3-month sum</strong> for that month. If an employee did not work for the previous two months, calculate their 3-month sum anyway, which will be equivalent to the sum of the salaries in the months they did work.</li>
	<li>Do not include the 3-month sum for the most recent month that the employee worked for that employee.</li>
	<li>Do not include the 3-month sum for any month the employee did not work.</li>
</ul>

<p>Return the result table ordered by <code>id</code> <strong>ascending</strong>. In case of a tie, order it by <code>month</code> <strong>descending</strong>.</p>

<p>The result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> 
Employee table:
+----+-------+--------+
| id | month | salary |
+----+-------+--------+
| 1  | 1     | 20     |
| 2  | 1     | 20     |
| 1  | 2     | 30     |
| 2  | 2     | 30     |
| 3  | 2     | 40     |
| 1  | 3     | 40     |
| 3  | 3     | 60     |
| 1  | 4     | 60     |
| 3  | 4     | 70     |
| 1  | 7     | 90     |
| 1  | 8     | 90     |
+----+-------+--------+
<strong>Output:</strong> 
+----+-------+--------+
| id | month | Salary |
+----+-------+--------+
| 1  | 7     | 90     |
| 1  | 4     | 130    |
| 1  | 3     | 90     |
| 1  | 2     | 50     |
| 1  | 1     | 20     |
| 2  | 1     | 20     |
| 3  | 3     | 100    |
| 3  | 2     | 40     |
+----+-------+--------+
<strong>Explanation:</strong> 
Employee 1 worked in months 1, 2, 3, 4, 7, and 8.
Their most recent month, 8, is excluded from the result.
Month 7 has no data in months 5 and 6, so its 3-month sum is just its own salary, 90.
Month 4's 3-month sum is 40 + 60 + 30 = 130.
Month 3's 3-month sum is 20 + 30 + 40 = 90.
Month 2's 3-month sum is 20 + 30 = 50 (month 0 doesn't exist).
Month 1's 3-month sum is just its own salary, 20.

Employee 2 worked in months 1 and 2. Their most recent month, 2, is excluded
from the result. Month 1's 3-month sum is just its own salary, 20.

Employee 3 worked in months 2, 3, and 4. Their most recent month, 4, is
excluded. Month 3's 3-month sum is 40 + 60 = 100 (month 1 doesn't exist for
employee 3). Month 2's 3-month sum is just its own salary, 40.
</pre>

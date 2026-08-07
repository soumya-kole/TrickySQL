# [2004. The Number of Seniors and Juniors to Join the Company](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company)

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
employee_id is the primary key (column with unique values) for this table.
experience is an ENUM (category) type of value ('Senior', 'Junior').
Each row of this table indicates the id of a candidate, their monthly salary, and their experience.
</pre>

<p>&nbsp;</p>

<p>A company wants to hire new employees. The budget of the company for the salaries is <code>$70000</code>. The company's criteria for hiring are:</p>

<ul>
	<li>Hire the <strong>largest number</strong> of seniors possible within the budget.</li>
	<li>After hiring the maximum number of seniors, use the remaining budget to hire the <strong>largest number</strong> of juniors possible.</li>
</ul>

<p>Write a solution to find the number of seniors and juniors hired under the mentioned criteria.</p>

<p>Return the result table in <strong>any order</strong>.</p>

<p>The result format is shown in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> 
Candidates table:
+-------------+------------+--------+
| employee_id | experience | salary |
+-------------+------------+--------+
| 1           | Junior     | 10000  |
| 9           | Junior     | 10000  |
| 2           | Senior     | 20000  |
| 11          | Senior     | 20000  |
| 13          | Senior     | 50000  |
| 4           | Junior     | 40000  |
+-------------+------------+--------+
<strong>Output:</strong> 
+------------+----------------------+
| experience | accepted_candidates  |
+------------+----------------------+
| Senior     | 2                    |
| Junior     | 2                    |
+------------+----------------------+
<strong>Explanation:</strong> 
We can hire 2 seniors with IDs (2, 11). Since the budget is $70000 and the sum of their salaries is $40000, we still have $30000 but they are not enough to hire the senior candidate with ID 13.
We can hire 2 juniors with IDs (1, 9). Since the remaining budget is $30000 and the sum of their salaries is $20000, we still have $10000 but they are not enough to hire the junior candidate with ID 4.
</pre>

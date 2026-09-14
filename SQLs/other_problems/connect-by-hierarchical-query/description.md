# Hierarchical Query in MySQL (CONNECT BY equivalent)

Oracle's `CONNECT BY` has no direct equivalent in MySQL; a recursive CTE does the same
job — walk a self-referencing `manager_id` column outward from the root to build an
org-chart hierarchy.

## Description

<p>Table: <code>employees</code></p>

<pre>
+-------------+-------------+
| Column Name | Type        |
+-------------+-------------+
| id          | int         |
| name        | varchar     |
| manager_id  | int         |
+-------------+-------------+
id is the primary key for this table.
manager_id references the id of the employee's manager; NULL for the top-level
employee (the CEO, who has no manager).
</pre>

<p>Write a query that returns every employee's <code>hierarchy_level</code> (0 for the
top-level employee, incrementing by 1 for each level below) and a
<code>hierarchy_path</code> showing the chain of names from the top down to that
employee, joined by <code>--></code>. Order the result by <code>hierarchy_level</code>,
then <code>id</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
employees table:
+----+-----------------+------------+
| id | name            | manager_id |
+----+-----------------+------------+
| 1  | CEO             | NULL       |
| 2  | CTO             | 1          |
| 3  | CFO             | 1          |
| 4  | Manager A       | 1          |
| 5  | Manager B       | 1          |
| 6  | Employee 1      | 4          |
| 7  | Employee 2      | 4          |
| 8  | Employee 3      | 5          |
| 9  | Employee 4      | 5          |
| 10 | Lead Developer  | 2          |
| 11 | Developer 1     | 10         |
| 12 | Developer 2     | 10         |
| 13 | Finance Manager | 3          |
| 14 | Accountant 1    | 13         |
| 15 | Accountant 2    | 13         |
+----+-----------------+------------+
<strong>Output:</strong>
+----+-----------------+------------+------------------+-------------------------------------+
| id | name            | manager_id | hierarchy_level  | hierarchy_path                       |
+----+-----------------+------------+------------------+-------------------------------------+
| 1  | CEO             | NULL       | 0                | CEO                                   |
| 2  | CTO             | 1          | 1                | CEO-->CTO                             |
| 3  | CFO             | 1          | 1                | CEO-->CFO                             |
| 4  | Manager A       | 1          | 1                | CEO-->Manager A                       |
| 5  | Manager B       | 1          | 1                | CEO-->Manager B                       |
| 6  | Employee 1      | 4          | 2                | CEO-->Manager A-->Employee 1          |
| 7  | Employee 2      | 4          | 2                | CEO-->Manager A-->Employee 2          |
| 8  | Employee 3      | 5          | 2                | CEO-->Manager B-->Employee 3          |
| 9  | Employee 4      | 5          | 2                | CEO-->Manager B-->Employee 4          |
| 10 | Lead Developer  | 2          | 2                | CEO-->CTO-->Lead Developer            |
| 13 | Finance Manager | 3          | 2                | CEO-->CFO-->Finance Manager           |
| 11 | Developer 1     | 10         | 3                | CEO-->CTO-->Lead Developer-->Developer 1     |
| 12 | Developer 2     | 10         | 3                | CEO-->CTO-->Lead Developer-->Developer 2     |
| 14 | Accountant 1    | 13         | 3                | CEO-->CFO-->Finance Manager-->Accountant 1   |
| 15 | Accountant 2    | 13         | 3                | CEO-->CFO-->Finance Manager-->Accountant 2   |
+----+-----------------+------------+------------------+-------------------------------------+
<strong>Explanation:</strong>
The CEO (id 1) is the only row with a NULL manager_id, so it is the root at level 0.
Each level below adds one more step to hierarchy_path: e.g. Developer 1 (id 11) reports
to Lead Developer (id 10), who reports to CTO (id 2), who reports to CEO — three hops
below the root, hence hierarchy_level 3.
</pre>

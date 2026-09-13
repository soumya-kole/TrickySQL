# Split Full Name into First/Middle/Last

Given a table of full names with a varying number of space-separated parts (one, two, or three), split each into `first_name`, `second_name`, and `last_name` columns.

## Description

<p>Table: <code>customers</code></p>

<pre>
+---------------+-------------+
| Column Name   | Type        |
+---------------+-------------+
| customer_name | varchar(30) |
+---------------+-------------+
Each row holds a full name with one, two, or three space-separated parts
(first name only, first + last, or first + middle + last).
</pre>

<p>Split each <code>customer_name</code> into <code>first_name</code>, <code>second_name</code>, and <code>last_name</code>:</p>

<ul>
	<li><code>first_name</code> is always the first word.</li>
	<li>If the name has only one word, both <code>second_name</code> and <code>last_name</code> are empty.</li>
	<li>If the name has exactly two words, <code>second_name</code> is empty and <code>last_name</code> is the second word.</li>
	<li>If the name has three words, <code>second_name</code> is the middle word and <code>last_name</code> is the last word.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
customers table:
+--------------------+
| customer_name      |
+--------------------+
| Soumya Kole        |
| Akash Kumar Singh  |
| Tom                |
+--------------------+
<strong>Output:</strong>
+--------------------+------------+-------------+-----------+
| customer_name      | first_name | second_name | last_name |
+--------------------+------------+-------------+-----------+
| Soumya Kole        | Soumya     |             | Kole      |
| Akash Kumar Singh  | Akash      | Kumar       | Singh     |
| Tom                | Tom        |             |           |
+--------------------+------------+-------------+-----------+
</pre>

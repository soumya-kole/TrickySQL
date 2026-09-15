# [1369. Get the Second Most Recent Activity 🔒](https://leetcode.com/problems/get-the-second-most-recent-activity)

## Description

<p>Table: <code>UserActivity</code></p>

<pre>
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| username      | varchar |
| activity      | varchar |
| startDate     | date    |
| endDate       | date    |
+---------------+---------+
This table may have duplicate rows.
This table contains information about the activities that have occurred in a company.
</pre>

<p>&nbsp;</p>

<p>Write a solution to show the second most recent activity of each user.
If the user only has one activity, return that one.</p>

<p>A user can't perform more than one activity at the same time.</p>

<p>Return the result table in <strong>any order</strong>.</p>

<p>The result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
UserActivity table:
+------------+--------------+-------------+-------------+
| username   | activity     | startDate   | endDate     |
+------------+--------------+-------------+-------------+
| Alice      | Travel       | 2020-02-12  | 2020-02-20  |
| Alice      | Dancing      | 2020-02-21  | 2020-02-23  |
| Alice      | Travel       | 2020-02-24  | 2020-02-28  |
| Bob        | Travel       | 2020-02-11  | 2020-02-18  |
+------------+--------------+-------------+-------------+
<strong>Output:</strong>
+------------+--------------+-------------+-------------+
| username   | activity     | startDate   | endDate     |
+------------+--------------+-------------+-------------+
| Alice      | Dancing      | 2020-02-21  | 2020-02-23  |
| Bob        | Travel       | 2020-02-11  | 2020-02-18  |
+------------+--------------+-------------+-------------+
<strong>Explanation:</strong>
Alice's most recent activity is "Travel", from 2020-02-24 to 2020-02-28.
Her second most recent activity is "Dancing", from 2020-02-21 to 2020-02-23.
Bob only has one activity, so it is returned.
</pre>

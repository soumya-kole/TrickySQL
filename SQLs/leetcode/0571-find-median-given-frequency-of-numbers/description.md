# [571. Find Median Given Frequency of Numbers 🔒](https://leetcode.com/problems/find-median-given-frequency-of-numbers)

## Description

<p>Table: <code>Numbers</code></p>

<pre>
+-------------+------+
| Column Name | Type |
+-------------+------+
| num         | int  |
| frequency   | int  |
+-------------+------+
</pre>

<p>num is the primary key (column with unique values) for this table.</p>

<p>Each row of this table shows the number <code>num</code> and how many times it appears in an array (its <code>frequency</code>). The array is the <em>decompressed</em> form of this frequency table.</p>

<p>Write a solution to report the <strong>median</strong> of the numbers in the decompressed array. The median of an array of even length is the average of the two middle values. Round the answer to <strong>one decimal place</strong>.</p>

<p>The result format is in the following example.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
Numbers table:
+-----+-----------+
| num | frequency |
+-----+-----------+
| 0   | 7         |
| 1   | 1         |
| 2   | 3         |
| 3   | 1         |
+-----+-----------+
<strong>Output:</strong>
+--------+
| median |
+--------+
| 0.0    |
+--------+
<strong>Explanation:</strong>
The decompressed array is [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3].
It has 12 elements, so the median is the average of the two middle values, both 0, giving 0.0.
</pre>

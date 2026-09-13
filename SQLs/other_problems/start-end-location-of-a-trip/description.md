# Start and End Location of a Trip

Each customer's trip is broken into consecutive legs, where one leg's `end_loc` matches the next leg's `start_loc`. Given the legs in any order, find each customer's overall starting and ending location.

## Description

<p>Table: <code>travel_data</code></p>

<pre>
+-------------+-------------+
| Column Name | Type        |
+-------------+-------------+
| customer    | varchar(10) |
| start_loc   | varchar(50) |
| end_loc     | varchar(50) |
+-------------+-------------+
Each row is one leg of a customer's trip. A customer's legs chain together
(one leg's end_loc is another leg's start_loc) into a single continuous
path with no branches or cycles.
</pre>

<p>For each customer, return the <code>start_loc</code> that never appears as an <code>end_loc</code> (the overall trip start) and the <code>end_loc</code> that never appears as a <code>start_loc</code> (the overall trip end).</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong>
travel_data table:
+----------+-----------+-----------+
| customer | start_loc | end_loc   |
+----------+-----------+-----------+
| c1       | New York  | Lima      |
| c1       | London    | New York  |
| c1       | Lima      | Sao Paulo |
| c1       | Sao Paulo | New Delhi |
| c2       | Mumbai    | Hyderabad |
| c2       | Surat     | Pune      |
| c2       | Hyderabad | Surat     |
| c3       | Kochi     | Kurnool   |
| c3       | Lucknow   | Agra      |
| c3       | Agra      | Jaipur    |
| c3       | Jaipur    | Kochi     |
+----------+-----------+-----------+
<strong>Output:</strong>
+----------+-----------+-----------+
| customer | start_loc | end_loc   |
+----------+-----------+-----------+
| c1       | London    | New Delhi |
| c2       | Mumbai    | Pune      |
| c3       | Lucknow   | Kurnool   |
+----------+-----------+-----------+
<strong>Explanation:</strong>
c1's legs chain as London -> New York -> Lima -> Sao Paulo -> New Delhi, so the trip starts at London and ends at New Delhi.
c2's legs chain as Mumbai -> Hyderabad -> Surat -> Pune.
c3's legs chain as Lucknow -> Agra -> Jaipur -> Kochi -> Kurnool.
</pre>

# 1412. Find the Quiet Students in All Exams - Solutions

## Solution 1: `RANK` both directions per exam, then check for zero extremes

A "quiet" student is one who, across every exam they sat, was never the (possibly tied) highest or lowest scorer. Ranking each exam's scores both ascending (`rk1`) and descending (`rk2`) marks the low end with `rk1 = 1` and the high end with `rk2 = 1` — ties get the same rank, so a tied extreme is still flagged, matching exam 20 in the example where student 1 alone holds both ends.

`RANK()` (not `ROW_NUMBER()`) is what makes ties count as extremes rather than only the first-seen row. After joining `Student` to filter to students who actually sat at least one exam, grouping by student and requiring zero `rk1 = 1` and zero `rk2 = 1` rows across all their exams identifies students who were always mid-pack.

#### MySQL

```sql
WITH ranked AS (
    SELECT
        student_id,
        RANK() OVER (PARTITION BY exam_id ORDER BY score)      AS rk_low,
        RANK() OVER (PARTITION BY exam_id ORDER BY score DESC) AS rk_high
    FROM Exam
)
SELECT s.student_id, s.student_name
FROM ranked r
JOIN Student s ON s.student_id = r.student_id
GROUP BY s.student_id, s.student_name
HAVING SUM(r.rk_low = 1) = 0 AND SUM(r.rk_high = 1) = 0
ORDER BY s.student_id;
```

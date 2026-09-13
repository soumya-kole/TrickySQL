# 1280. Students and Examinations - Solutions

## Solution 1: Cross Join + Pre-Aggregated Left Join

Build every valid `(student, subject)` combination first with a `CROSS JOIN` between `Students` and `Subjects`, since each student is expected to take every subject. Separately, aggregate `Examinations` down to one row per `(student_id, subject_name)` with its attendance count, then `LEFT JOIN` that onto the combination set. Aggregating before the join keeps the join itself small — at most one matching row per combination — rather than joining the raw `Examinations` rows and grouping afterward, which lets a heavily-repeated exam fan out the intermediate result first. `COALESCE` turns the `NULL` count from unmatched combinations into `0`.

#### MySQL

```sql
SELECT
    c.student_id,
    c.student_name,
    c.subject_name,
    COALESCE(e.attended_exams, 0) AS attended_exams
FROM (
    SELECT student_id, student_name, subject_name
    FROM Students
    CROSS JOIN Subjects
) c
LEFT JOIN (
    SELECT student_id, subject_name, COUNT(*) AS attended_exams
    FROM Examinations
    GROUP BY student_id, subject_name
) e
    ON c.student_id = e.student_id AND c.subject_name = e.subject_name
ORDER BY c.student_id, c.subject_name;
```

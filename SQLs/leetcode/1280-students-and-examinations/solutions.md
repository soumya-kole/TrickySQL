# 1280. Students and Examinations - Solutions

## Solution 1: Cross Join + Left Join, Then Aggregate

Build every `(student, subject)` combination in a CTE with a `CROSS JOIN`, then `LEFT JOIN`
the raw `Examinations` rows onto it and group afterward. Each combination is joined to all
of its exam rows (or to a single all-`NULL` row if there are none), and `GROUP BY` collapses
them back to one row per combination.

The zero count comes from `COUNT(ex.subject_name)` rather than `COALESCE`. `COUNT` of a
column skips `NULL`s, so a combination with no matching exam, whose joined
`ex.subject_name` is `NULL`, counts as 0. `COUNT(*)` would count that all-`NULL` row and
wrongly return 1.

`student_name` is in the `GROUP BY` only so it can be selected. It never splits a group,
because each `student_id` has exactly one name.

Compared with Solution 2, this is shorter, but the join runs on the raw exam rows, so a
heavily repeated exam makes the intermediate result larger before grouping shrinks it.

#### MySQL

```sql
WITH student_subjects AS (
    SELECT
        st.student_id,
        st.student_name,
        sub.subject_name
    FROM Students st
    CROSS JOIN Subjects sub
)
SELECT
    ss.student_id,
    ss.student_name,
    ss.subject_name,
    COUNT(ex.subject_name) AS attended_exams
FROM student_subjects ss
LEFT JOIN Examinations ex
    ON ss.student_id = ex.student_id AND ss.subject_name = ex.subject_name
GROUP BY ss.student_id, ss.student_name, ss.subject_name
ORDER BY ss.student_id, ss.subject_name;
```

## Solution 2: Cross Join + Pre-Aggregated Left Join

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

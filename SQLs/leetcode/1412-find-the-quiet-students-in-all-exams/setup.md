# 1412. Find the Quiet Students in All Exams - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Exam;
DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    student_id   INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE Exam (
    exam_id    INT,
    student_id INT,
    score      INT,
    PRIMARY KEY (exam_id, student_id)
);

INSERT INTO Student (student_id, student_name) VALUES
(1, 'Daniel'),
(2, 'Jade'),
(3, 'Stella'),
(4, 'Jonathan'),
(5, 'Will');

INSERT INTO Exam (exam_id, student_id, score) VALUES
(10, 1, 70),
(10, 2, 80),
(10, 3, 90),
(20, 1, 80),
(30, 1, 70),
(30, 3, 80),
(30, 4, 90),
(40, 1, 60),
(40, 2, 70),
(40, 4, 80);
```

Load this dataset:

```bash
make setup 1412-find-the-quiet-students-in-all-exams
```

# 618. Students Report By Geography - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    name      VARCHAR(50),
    continent VARCHAR(50)
);

INSERT INTO Student (name, continent) VALUES
('Jane', 'America'),
('Pascal', 'Europe'),
('Xi', 'Asia'),
('Jack', 'America');
```

Load this dataset:

```bash
make setup 0618-students-report-by-geography
```

## Setup2

Edge case for the follow-up: America is *not* the continent with the most students (Asia is).

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    name      VARCHAR(50),
    continent VARCHAR(50)
);

INSERT INTO Student (name, continent) VALUES
('Jane', 'America'),
('Jack', 'America'),
('Pascal', 'Europe'),
('Xi', 'Asia'),
('Mo', 'Asia'),
('Ravi', 'Asia'),
('Sam', 'Asia');
```

Load this dataset:

```bash
make setup 0618-students-report-by-geography 2
```

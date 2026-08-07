# 1767. Find the Subtasks That Did Not Execute - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Executed;
DROP TABLE IF EXISTS Tasks;

CREATE TABLE Tasks (
    task_id        INT PRIMARY KEY,
    subtasks_count INT
);

CREATE TABLE Executed (
    task_id    INT,
    subtask_id INT,
    PRIMARY KEY (task_id, subtask_id)
);

INSERT INTO Tasks (task_id, subtasks_count) VALUES
(1, 3),
(2, 2),
(3, 4);

INSERT INTO Executed (task_id, subtask_id) VALUES
(1, 2),
(3, 1),
(3, 2),
(3, 3),
(3, 4);
```

Load this dataset:

```bash
make setup 1767-find-the-subtasks-that-did-not-execute
```

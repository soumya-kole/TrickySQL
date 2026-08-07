# 1767. Find the Subtasks That Did Not Execute - Solutions

## Solution 1: Recursive CTE

#### MySQL

```sql
WITH RECURSIVE cte AS (
    SELECT task_id, 1 AS subtask_id FROM Tasks
    UNION ALL
    SELECT task_id, subtask_id + 1 AS subtask_id FROM cte c
    WHERE subtask_id < (SELECT subtasks_count FROM Tasks WHERE task_id = c.task_id)
)
SELECT task_id, subtask_id FROM cte c
WHERE NOT EXISTS (
    SELECT 1 FROM Executed e
    WHERE c.task_id = e.task_id AND c.subtask_id = e.subtask_id
);
```

The recursive CTE seeds one row per task at `subtask_id = 1`, then grows each task's chain independently, stopping once `subtask_id` reaches that task's own `subtasks_count`. This generates exactly the valid subtask IDs for every task. `NOT EXISTS` against `Executed` then keeps only the subtasks that were never run successfully.

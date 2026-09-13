# 1264. Page Recommendations - Solutions

## Solution 1: Union both friendship directions, then join `Likes`

`Friendship` stores each pair once, but friendship is symmetric, so user 1's friends can sit in either column. `UNION` both queries (one per column) into a single friend list `T`, join it to `Likes` to get everything a friend likes, and drop anything user 1 already likes with `NOT IN`.

#### MySQL

```sql
WITH friends AS (
    SELECT user2_id AS user_id FROM Friendship WHERE user1_id = 1
    UNION
    SELECT user1_id AS user_id FROM Friendship WHERE user2_id = 1
)
SELECT DISTINCT l.page_id AS recommended_page
FROM friends f
JOIN Likes l ON l.user_id = f.user_id
WHERE l.page_id NOT IN (SELECT page_id FROM Likes WHERE user_id = 1);
```

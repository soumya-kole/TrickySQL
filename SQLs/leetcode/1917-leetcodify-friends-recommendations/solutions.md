# 1917. Leetcodify Friends Recommendations - Solutions

## Solution 1: Self-join `Listens` on shared day/song, exclude existing friends

Self-join `Listens` to itself on matching `day` and `song_id` with `user_id != user_id` to line up every pair of (distinct) users who listened to the same song on the same day. Grouping by `(day, user_id, recommended_id)` and requiring `COUNT(DISTINCT song_id) >= 3` keeps only pairs who shared at least three different songs on that day; `DISTINCT` on the final `SELECT` then collapses a pair that qualifies on more than one day down to a single recommendation row.

`Friendship` only stores `user1_id < user2_id`, so it's unioned with its own reverse before the `NOT EXISTS` check — otherwise a friendship would only ever be excluded in one direction.

#### MySQL

```sql
WITH bidirectional_friendship AS (
    SELECT user1_id, user2_id FROM Friendship
    UNION
    SELECT user2_id AS user1_id, user1_id AS user2_id FROM Friendship
)
SELECT DISTINCT
    l1.user_id,
    l2.user_id AS recommended_id
FROM Listens l1
JOIN Listens l2
    ON l1.day = l2.day
    AND l1.song_id = l2.song_id
    AND l1.user_id != l2.user_id
WHERE NOT EXISTS (
    SELECT 1
    FROM bidirectional_friendship f
    WHERE f.user1_id = l1.user_id AND f.user2_id = l2.user_id
)
GROUP BY l1.day, l1.user_id, l2.user_id
HAVING COUNT(DISTINCT l1.song_id) >= 3;
```

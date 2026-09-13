# 1892. Page Recommendations II - Solutions

## Solution 1: Bidirectional friendship + `NOT EXISTS` + count

This is [1264. Page Recommendations](../1264-page-recommendations/solutions.md) generalized to every user and with a per-page friend count. `Friendship` only stores each pair once, so union it with its own reverse to get every user paired with each of their friends in both directions.

Joining that bidirectional list to `Likes` (on the friend's side) gives every `(user, page)` a friend likes. `NOT EXISTS` drops the pages the user already likes themselves, and grouping by `(user_id, page_id)` turns "how many friends liked it" into a plain `COUNT(*)`.

#### MySQL

```sql
WITH bidirectional_friendship AS (
    SELECT user1_id, user2_id FROM Friendship
    UNION
    SELECT user2_id AS user1_id, user1_id AS user2_id FROM Friendship
)
SELECT
    f.user1_id AS user_id,
    l.page_id,
    COUNT(*) AS friends_likes
FROM bidirectional_friendship f
JOIN Likes l ON l.user_id = f.user2_id
WHERE NOT EXISTS (
    SELECT 1
    FROM Likes own
    WHERE own.user_id = f.user1_id AND own.page_id = l.page_id
)
GROUP BY f.user1_id, l.page_id;
```

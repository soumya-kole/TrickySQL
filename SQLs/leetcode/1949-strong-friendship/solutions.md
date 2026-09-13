# 1949. Strong Friendship - Solutions

## Solution 1: Triangle join over the bidirectional edge list

`Friendship` only stores each pair once (with `user1_id < user2_id`), but "who is friends with whom" needs to be looked up from either side, so first union it with its own reverse into a bidirectional edge list `e`.

A common friend of `u` and `v` is a third user `w` reachable as an edge from both `u` and `v` — i.e. a triangle `u–w`, `v–w`. Self-joining `e` three ways (`a`: `u→v` the candidate pair, `b`: `u→w`, `c`: `v→w`, matching `b`'s and `c`'s far end) counts exactly those triangles per pair. Filtering `a.user1_id < a.user2_id` keeps one row per unordered pair, and `HAVING COUNT(*) >= 3` applies the "strong" threshold.

#### MySQL

```sql
WITH bidirectional_friendship AS (
    SELECT user1_id, user2_id FROM Friendship
    UNION
    SELECT user2_id AS user1_id, user1_id AS user2_id FROM Friendship
)
SELECT
    pair.user1_id,
    pair.user2_id,
    COUNT(*) AS common_friend
FROM bidirectional_friendship pair
JOIN bidirectional_friendship u_side ON u_side.user1_id = pair.user1_id
JOIN bidirectional_friendship v_side
    ON v_side.user1_id = pair.user2_id
    AND v_side.user2_id = u_side.user2_id
WHERE pair.user1_id < pair.user2_id
GROUP BY pair.user1_id, pair.user2_id
HAVING COUNT(*) >= 3;
```

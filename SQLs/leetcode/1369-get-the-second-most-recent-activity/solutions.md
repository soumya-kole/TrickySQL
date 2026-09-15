# 1369. Get the Second Most Recent Activity - Solutions

## Solution 1: Deduplicate, then ROW_NUMBER with a per-user count

`UserActivity` "may have duplicate rows" — exact-duplicate rows are the same
activity occurrence recorded twice, not two distinct activities. Ranking raw
rows with `ROW_NUMBER() OVER (PARTITION BY username ORDER BY startDate DESC)`
without removing duplicates first is unsafe: if the *most recent* activity
happens to be duplicated, its two copies claim ranks `1` and `2`, burying the
true second-most-recent (older) activity at rank `3` and never returning it.
The fix is to collapse duplicates with `SELECT DISTINCT` before ranking, so
every distinct activity is counted exactly once regardless of how many times
its row appears in the raw table.

Since a user "can't perform more than one activity at the same time", no two
of a user's *distinct* activities share a `startDate`, so ranking the
deduplicated rows by `startDate DESC` is unambiguous, and the row numbered `2`
is always the second most recent activity. `cnt` (a count of each user's
distinct activities) then handles the fallback: a user with only one distinct
activity has no row numbered `2`, so `cnt = 1` keeps their single (`rk = 1`)
row instead of dropping them.

#### MySQL

```sql
SELECT username, activity, startDate, endDate
FROM (
    SELECT
        username,
        activity,
        startDate,
        endDate,
        ROW_NUMBER() OVER (PARTITION BY username ORDER BY startDate DESC) AS rk,
        COUNT(*) OVER (PARTITION BY username) AS cnt
    FROM (
        SELECT DISTINCT username, activity, startDate, endDate
        FROM UserActivity
    ) AS d
) AS t
WHERE rk = 2 OR cnt = 1;
```

**Step by step:**

1. **`d`** — `SELECT DISTINCT` collapses exact-duplicate rows so each real
   activity occurrence appears exactly once, regardless of how many times it
   was recorded in `UserActivity`.
2. **Window functions** — over the deduplicated rows, `rk` numbers each
   user's activities from most recent (`1`) to least recent `startDate`, and
   `cnt` repeats that user's total distinct-activity count on every one of
   their rows.
3. **Filter** — `rk = 2` picks the second most recent activity for users with
   two or more distinct activities; `cnt = 1` catches the single-activity
   users, whose only row is also `rk = 1`.

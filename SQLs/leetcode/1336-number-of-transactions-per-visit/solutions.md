# 1336. Number of Transactions per Visit - Solutions

## Solution 1: Recursive CTE for the axis, left-joined against per-visit transaction counts

The result must include every integer from `0` up to the largest transaction count seen on any single visit — even counts nobody actually hit (like `2` in the example) — so a plain `GROUP BY` on the data alone would silently skip empty buckets. A recursive CTE builds that complete `0..max` axis first.

Separately, `per_visit` counts transactions per `(user_id, transaction_date)` and left-joins that onto `Visits` so a visit with no transactions gets `COALESCE(..., 0)` instead of disappearing. Left-joining the axis to `per_visit` on a matching count, then grouping by the axis value, turns "how many visits had exactly `n` transactions" into a `COUNT` that correctly returns `0` for buckets no visit falls into — `COUNT(pv.user_id)` (not `COUNT(*)`) is what makes an empty bucket count as `0` rather than `1` for the unmatched join row.

#### MySQL

```sql
WITH RECURSIVE per_visit AS (
    SELECT
        v.user_id,
        v.visit_date,
        COALESCE(t.cnt, 0) AS txn_count
    FROM Visits v
    LEFT JOIN (
        SELECT user_id, transaction_date, COUNT(*) AS cnt
        FROM Transactions
        GROUP BY user_id, transaction_date
    ) t ON t.user_id = v.user_id AND t.transaction_date = v.visit_date
),
axis AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n + 1 FROM axis WHERE n < (SELECT MAX(txn_count) FROM per_visit)
)
SELECT
    axis.n AS transactions_count,
    COUNT(pv.user_id) AS visits_count
FROM axis
LEFT JOIN per_visit pv ON pv.txn_count = axis.n
GROUP BY axis.n
ORDER BY axis.n;
```

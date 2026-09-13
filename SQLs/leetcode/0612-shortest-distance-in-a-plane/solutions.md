# 612. Shortest Distance in a Plane - Solutions

## Solution 1: Self-join every pair, order by distance, take the smallest

Self-join `Point2D` to itself to form every pair of points, excluding a point paired with itself (`p1.x != p2.x OR p1.y != p2.y` — plain `p1 != p2` on the pair wouldn't be enough since either coordinate alone could differ while still being the same physical point only when both match). Euclidean distance is `SQRT` of the sum of squared coordinate differences; rounding to two decimals and taking the smallest via `ORDER BY ... LIMIT 1` gives the closest pair's distance.

Each pair is counted twice (once in each direction) and the identical distance appears twice, which doesn't affect the minimum.

#### MySQL

```sql
SELECT ROUND(SQRT(POW(p1.x - p2.x, 2) + POW(p1.y - p2.y, 2)), 2) AS shortest
FROM Point2D p1
JOIN Point2D p2 ON p1.x != p2.x OR p1.y != p2.y
ORDER BY shortest
LIMIT 1;
```

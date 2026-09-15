# 2173. Longest Winning Streak - Solutions

## Solution 1: Gaps-and-islands via row-number difference

A "winning streak" is a run of consecutive matches (by `match_day` order, not
calendar-consecutive days) that are all `'Win'`. The classic gaps-and-islands
trick for grouping runs of the *same* value is to compare two row numbers:
one over all of a player's matches, and one over just the matches sharing
that player's `result`. Within any unbroken run of a single `result`, both
numbers climb together, so their difference (`rk`) stays constant for the
whole run and changes only when the run breaks.

`T1` computes that difference. Grouping by `(player_id, rk)` in `T2` then
buckets each run together, and `SUM(result = 'Win')` counts how many rows in
that run are wins — which is either the full run length (if the run's result
is `'Win'`) or `0` (if it's a run of `'Draw'` or `'Lose'`, since none of its
rows are wins). Taking `MAX(s)` per player then picks out the longest run
that was all wins.

Every player in `Matches` is captured this way — even a player with zero
wins still has at least one `(player_id, rk)` group, contributing `s = 0`, so
no separate `COALESCE`/outer join is needed to produce their `0` row.

#### MySQL

```sql
WITH
    T1 AS (
        SELECT
            player_id,
            result,
            ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_day)
                - ROW_NUMBER() OVER (PARTITION BY player_id, result ORDER BY match_day) AS rk
        FROM Matches
    ),
    T2 AS (
        SELECT player_id, SUM(result = 'Win') AS s
        FROM T1
        GROUP BY player_id, rk
    )
SELECT player_id, MAX(s) AS longest_streak
FROM T2
GROUP BY player_id;
```

**Step by step:**

1. **`T1`** — for each match, subtract the player's per-`result` row number
   (ordered by `match_day`) from the player's overall row number (also
   ordered by `match_day`). Inside one unbroken run of the same `result`,
   both counters advance by 1 per row, so the difference `rk` is constant
   across the run; it shifts to a new value as soon as the result changes.
2. **`T2`** — grouping by `(player_id, rk)` collects each run into one row.
   `SUM(result = 'Win')` counts the wins in that run, which is the run's
   full length for a winning run and `0` otherwise (a run can only contain
   one kind of result, by construction of `rk`).
3. **Final `SELECT`** — `MAX(s)` per `player_id` is the longest all-win run;
   players with no wins at all still appear, with every run contributing
   `s = 0`.

> **Follow up (win-or-draw streaks):** replace `result = 'Win'` with
> `result <> 'Lose'` in `T2`'s `SUM`, but first fold `'Win'` and `'Draw'`
> into a single category *before* computing `rk` in `T1` (e.g. partition
> `T1`'s second `ROW_NUMBER()` by `player_id, result <> 'Lose'` instead of
> `player_id, result`) — otherwise a `Win, Draw, Win` sequence would still
> split into separate runs instead of counting as one streak of 3.

---
name: sql-style-conventions
description: House style conventions for writing or reviewing MySQL solution SQL in this repo (SQLs/leetcode, SQLs/other_problems, SQLs/*.md, Concepts/*.md). Use whenever writing, editing, or reviewing solution SQL, or a solutions.md file.
---

# SQL style conventions

These are style preferences for solution SQL in this repo — not correctness rules, since MySQL accepts the alternatives too. Apply them proactively when writing new solutions, not just when corrected.

## Prefer CASE over IF / GREATEST / LEAST

Use `CASE WHEN <condition> THEN <value> ... END` instead of MySQL-specific conditional shortcut functions:

- `IF(<condition>, <value>, NULL)` → `MAX(CASE WHEN continent = 'America' THEN name END)` instead of `MAX(IF(continent = 'America', name, NULL))`
- `GREATEST(a, b)` → `CASE WHEN a > b THEN a ELSE b END`
- `LEAST(a, b)` → `CASE WHEN a < b THEN a ELSE b END`

Applies to pivots, conditional aggregation, plain conditional value selection, and picking the larger/smaller of two expressions. If an existing file has both a shortcut-function solution and a near-duplicate `CASE` solution demonstrating the same technique, collapse them into one `CASE` solution rather than keeping both.

## Prefer SUBDATE/ADDDATE over DATE_SUB/DATE_ADD

`SUBDATE`/`ADDDATE` are synonyms for `DATE_SUB`/`DATE_ADD` when called with an `INTERVAL` expression, but they also accept a plain-integer-days shorthand (`SUBDATE(date, 7)`), which `DATE_SUB`/`DATE_ADD` do not — `DATE_SUB('2026-09-15', 7)` is a MySQL syntax error, while `SUBDATE('2026-09-15', 7)` works. `SUBDATE`/`ADDDATE` are a strict superset of what `DATE_SUB`/`DATE_ADD` can do, so use them whether shifting by a plain integer or by an `INTERVAL`. Documented in this repo at `Concepts/Date_Functions.md`, Step 2.

## Prefer the full ROWS BETWEEN form

Spell out `ROWS BETWEEN n PRECEDING AND CURRENT ROW` (or the appropriate `BETWEEN ... AND ...` bounds) rather than the single-sided shorthand `ROWS n PRECEDING`, even though MySQL accepts both. The explicit `BETWEEN ... AND CURRENT ROW` reads more clearly to someone unfamiliar with the shorthand.

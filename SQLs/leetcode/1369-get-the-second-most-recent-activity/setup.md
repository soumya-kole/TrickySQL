# 1369. Get the Second Most Recent Activity - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS UserActivity;

CREATE TABLE UserActivity (
    username  VARCHAR(30),
    activity  VARCHAR(30),
    startDate DATE,
    endDate   DATE
);

INSERT INTO UserActivity (username, activity, startDate, endDate) VALUES
('Alice', 'Travel',  '2020-02-12', '2020-02-20'),
('Alice', 'Dancing', '2020-02-21', '2020-02-23'),
('Alice', 'Travel',  '2020-02-24', '2020-02-28'),
('Bob',   'Travel',  '2020-02-11', '2020-02-18');
```

Load this dataset:

```bash
make setup 1369-get-the-second-most-recent-activity
```

## Setup2

The problem statement notes that `UserActivity` "may have duplicate rows" —
exact-duplicate rows represent the *same* activity occurrence, not two
distinct ones. This dataset exercises that: `Bob` has one distinct activity
duplicated across two rows; `XXX` has a duplicate on a middle-ranked activity;
and `Zed` has a duplicate on the *most recent* activity, which is the case
that breaks a solution that ranks rows without deduplicating first (see
Solution 1).

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS UserActivity;

CREATE TABLE UserActivity (
    username  VARCHAR(30),
    activity  VARCHAR(30),
    startDate DATE,
    endDate   DATE
);

INSERT INTO UserActivity (username, activity, startDate, endDate) VALUES
('Alice', 'Travel',  '2020-02-12', '2020-02-20'),
('Alice', 'Dancing', '2020-02-21', '2020-02-23'),
('Alice', 'Travel',  '2020-02-24', '2020-02-28'),
('Bob',   'Travel',  '2020-02-11', '2020-02-18'),
('Bob',   'Travel',  '2020-02-11', '2020-02-18'),
('XXX',   'Travel',  '2020-02-12', '2020-02-20'),
('XXX',   'Travel',  '2020-02-12', '2020-02-20'),
('XXX',   'Dancing', '2020-02-24', '2020-02-28'),
('XXX',   'Travel',  '2020-02-11', '2020-02-18'),
('XXX',   'Travel',  '2020-02-11', '2020-02-18'),
('Zed',   'Travel',  '2020-02-24', '2020-02-28'),
('Zed',   'Travel',  '2020-02-24', '2020-02-28'),
('Zed',   'Dancing', '2020-02-21', '2020-02-23');
```

Load this dataset:

```bash
make setup 1369-get-the-second-most-recent-activity 2
```

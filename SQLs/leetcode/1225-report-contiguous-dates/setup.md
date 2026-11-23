# 1225. Report Contiguous Dates - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Failed;
DROP TABLE IF EXISTS Succeeded;

CREATE TABLE Failed (
    fail_date DATE PRIMARY KEY
);

CREATE TABLE Succeeded (
    success_date DATE PRIMARY KEY
);

INSERT INTO Failed (fail_date) VALUES
('2018-12-28'),
('2018-12-29'),
('2019-01-04'),
('2019-01-05');

INSERT INTO Succeeded (success_date) VALUES
('2018-12-30'),
('2018-12-31'),
('2019-01-01'),
('2019-01-02'),
('2019-01-03'),
('2019-01-06');
```

Load this dataset:

```bash
make setup 1225-report-contiguous-dates
```

## Setup2

Alternating states: `failed`, `succeeded`, `failed` on three consecutive days.
It trips up a solution that groups by the rank difference alone, without the
state: the last two days share the same difference (`1`), so they get merged
into one interval.

Correct output, three one-day intervals:

| period_state | start_date | end_date   |
| ------------ | ---------- | ---------- |
| failed       | 2019-01-01 | 2019-01-01 |
| succeeded    | 2019-01-02 | 2019-01-02 |
| failed       | 2019-01-03 | 2019-01-03 |

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Failed;
DROP TABLE IF EXISTS Succeeded;

CREATE TABLE Failed (
    fail_date DATE PRIMARY KEY
);

CREATE TABLE Succeeded (
    success_date DATE PRIMARY KEY
);

INSERT INTO Failed (fail_date) VALUES
('2019-01-01'),
('2019-01-03');

INSERT INTO Succeeded (success_date) VALUES
('2019-01-02');
```

Load this dataset:

```bash
make setup 1225-report-contiguous-dates 2
```

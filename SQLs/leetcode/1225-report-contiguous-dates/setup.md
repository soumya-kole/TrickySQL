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

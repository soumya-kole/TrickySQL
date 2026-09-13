# Match Win/Loss Summary - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS icc_world_cup;

CREATE TABLE icc_world_cup (
    Team_1 VARCHAR(20),
    Team_2 VARCHAR(20),
    Winner VARCHAR(20)
);

INSERT INTO icc_world_cup (Team_1, Team_2, Winner) VALUES
('India', 'SL', 'India'),
('SL', 'Aus', 'Aus'),
('SA', 'Eng', 'Eng'),
('Eng', 'NZ', 'NZ'),
('Aus', 'India', 'India');
```

Load this dataset:

```bash
make setup match-win-summary
```

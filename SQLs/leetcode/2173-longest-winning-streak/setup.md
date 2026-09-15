# 2173. Longest Winning Streak - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Matches;

CREATE TABLE Matches (
    player_id INT,
    match_day DATE,
    result    ENUM('Win', 'Draw', 'Lose'),
    PRIMARY KEY (player_id, match_day)
);

INSERT INTO Matches (player_id, match_day, result) VALUES
(1, '2022-01-17', 'Win'),
(1, '2022-01-18', 'Win'),
(1, '2022-01-25', 'Win'),
(1, '2022-01-31', 'Draw'),
(1, '2022-02-08', 'Win'),
(2, '2022-02-06', 'Lose'),
(2, '2022-02-08', 'Lose'),
(3, '2022-03-30', 'Win');
```

Load this dataset:

```bash
make setup 2173-longest-winning-streak
```

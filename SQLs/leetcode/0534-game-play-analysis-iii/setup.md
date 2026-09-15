# 534. Game Play Analysis III - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Activity;

CREATE TABLE Activity (
    player_id INT,
    device_id INT,
    event_date DATE,
    games_played INT,
    PRIMARY KEY (player_id, event_date)
);

INSERT INTO Activity (player_id, device_id, event_date, games_played) VALUES
(1, 2, '2016-03-01', 5),
(1, 2, '2016-05-02', 6),
(1, 3, '2017-06-25', 1),
(3, 1, '2016-03-02', 0),
(3, 4, '2018-07-03', 5);
```

Load this dataset:

```bash
make setup 0534-game-play-analysis-iii
```

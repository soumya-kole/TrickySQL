# 1917. Leetcodify Friends Recommendations - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Friendship;
DROP TABLE IF EXISTS Listens;

CREATE TABLE Listens (
    user_id INT,
    song_id INT,
    day     DATE
);

CREATE TABLE Friendship (
    user1_id INT,
    user2_id INT,
    PRIMARY KEY (user1_id, user2_id)
);

INSERT INTO Listens (user_id, song_id, day) VALUES
(1, 10, '2021-03-15'),
(1, 11, '2021-03-15'),
(1, 12, '2021-03-15'),
(2, 10, '2021-03-15'),
(2, 11, '2021-03-15'),
(2, 12, '2021-03-15'),
(3, 10, '2021-03-15'),
(3, 11, '2021-03-15'),
(3, 12, '2021-03-15'),
(4, 10, '2021-03-15'),
(4, 11, '2021-03-15'),
(4, 13, '2021-03-15'),
(5, 10, '2021-03-16'),
(5, 11, '2021-03-16'),
(5, 12, '2021-03-16');

INSERT INTO Friendship (user1_id, user2_id) VALUES
(1, 2);
```

Load this dataset:

```bash
make setup 1917-leetcodify-friends-recommendations
```

# 1949. Strong Friendship - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Friendship;

CREATE TABLE Friendship (
    user1_id INT,
    user2_id INT,
    PRIMARY KEY (user1_id, user2_id)
);

INSERT INTO Friendship (user1_id, user2_id) VALUES
(1, 2),
(1, 3),
(2, 3),
(1, 4),
(2, 4),
(1, 5),
(2, 5),
(1, 7),
(3, 7),
(1, 6),
(3, 6),
(2, 6);
```

Load this dataset:

```bash
make setup 1949-strong-friendship
```

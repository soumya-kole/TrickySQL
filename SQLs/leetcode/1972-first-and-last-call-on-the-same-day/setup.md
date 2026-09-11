# 1972. First and Last Call On the Same Day - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Calls;

CREATE TABLE Calls (
    caller_id    INT,
    recipient_id INT,
    call_time    DATETIME,
    PRIMARY KEY (caller_id, recipient_id, call_time)
);

INSERT INTO Calls (caller_id, recipient_id, call_time) VALUES
(8, 4, '2021-08-24 17:46:07'),
(4, 8, '2021-08-24 19:57:13'),
(5, 1, '2021-08-11 05:28:44'),
(8, 3, '2021-08-17 04:04:15'),
(11, 3, '2021-08-17 13:07:00'),
(8, 11, '2021-08-17 22:22:22');
```

Load this dataset:

```bash
make setup 1972-first-and-last-call-on-the-same-day
```

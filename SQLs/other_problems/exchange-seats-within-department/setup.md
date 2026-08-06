# Exchange Seats (within Department) - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Seat;

CREATE TABLE Seat (
    dept    VARCHAR(50),
    id      INT,
    student VARCHAR(50)
);

INSERT INTO Seat (dept, id, student) VALUES
('IT', 1, 'Abbot'),
('IT', 2, 'Doris'),
('IT', 3, 'Emerson'),
('IT', 4, 'Green'),
('IT', 5, 'Jeames'),
('EC', 1, 'AA'),
('EC', 2, 'BB'),
('EC', 3, 'CC'),
('EC', 4, 'DD');
```

Load this dataset:

```bash
make setup exchange-seats-within-department
```

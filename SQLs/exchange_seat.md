## Objective
This is similar to Leetcode problem [leetcode](https://leetcode.com/problems/exchange-seats/)
However, we added dept and seat must be exchanged withing the dept


## Data preparation

```sql
drop table demo.Seat;
Create table demo.Seat (dept varchar(50), id int, student varchar(50));
INSERT INTO demo.Seat (dept, id, student) VALUES
('IT', '1', 'Abbot'),
('IT', '2', 'Doris'),
('IT', '3', 'Emerson'),
('IT', '4', 'Green'),
('IT', '5', 'Jeames'),
('EC', '1', 'AA'),
('EC', '2', 'BB'),
('EC', '3', 'CC'),
('EC', '4', 'DD');
```

## Solution

```sql
WITH cte
     AS (SELECT *,
                Count(*)
                  OVER(
                    partition BY dept) AS cnt
         FROM   demo.Seat)
SELECT dept,
       CASE
         WHEN id%2 = 1
              AND id < cnt THEN id + 1
         WHEN id%2 = 1
              AND id = cnt THEN id
         ELSE id - 1
       END AS id,
       student
FROM   cte
ORDER  BY dept,
          id ;
```
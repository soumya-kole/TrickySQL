## Objective
This is Leetcode problem [leetcode](https://leetcode.com/problems/customers-with-strictly-increasing-purchases/)


## Data preparation

```sql
drop table demo.Orders;
Create table If Not Exists demo.Orders (order_id int, customer_id int, order_date date, price int);

insert into demo.Orders (order_id, customer_id, order_date, price) 
values ('1', '1', '2019-07-01', '1100')
,('2', '1', '2019-11-01', '1200')
,('3', '1', '2020-05-26', '3000')
,('4', '1', '2021-08-31', '3100')
,('5', '1', '2022-12-07', '4700')
,('6', '2', '2015-01-01', '700')
,('7', '2', '2017-11-07', '1000')
,('8', '3', '2017-01-01', '900')
,('9', '3', '2018-11-07', '900');
```

### Output expected
Only customer 1 has strictly increasing purchase

Explanation: 
Customer 1: The first year is 2019 and the last year is 2022
  - 2019: 1100 + 1200 = 2300
  - 2020: 3000
  - 2021: 3100
  - 2022: 4700
  We can see that the total purchases are strictly increasing yearly, so we include customer 1 in the answer.

Customer 2: The first year is 2015 and the last year is 2017
  - 2015: 700
  - 2016: 0
  - 2017: 1000
  We do not include customer 2 in the answer because the total purchases are not strictly increasing. Note that customer 2 did not make any purchases in 2016.

Customer 3: The first year is 2017, and the last year is 2018
  - 2017: 900
  - 2018: 900
 We do not include customer 3 in the answer because the total purchases are not strictly increasing.

### Solution approach

Eliminate missing year
  - If we take max and min year for each customer and count the number of years the customer purchased then max year - min year should be same as count of year count+1

Eliminate decresing purchase
  - Once we eliminate the missing year, if we rank the year and purchase for each customer, both of them should be in tandem if purchase has increased as year will be increase

### Final query
```sql
WITH cte AS
  (SELECT customer_id,
          year(order_date) AS order_year,
          sum(price) AS total_price
   FROM demo.Orders
   GROUP BY customer_id,
            year(order_date)),
     cte2 AS
  (SELECT customer_id,
          total_price,
          order_year,
          max(order_year) OVER (PARTITION BY customer_id) AS max_year,
                               min(order_year) OVER (PARTITION BY customer_id) AS min_year,
                                                    count(order_year) OVER (PARTITION BY customer_id) AS cnt
   FROM cte),
     cte3 AS
  (SELECT *
   FROM cte2
   WHERE cnt = max_year - min_year + 1 ),
     cte4 AS
  (SELECT *,
          rank() over(PARTITION BY customer_id
                      ORDER BY total_price) AS price_rnk,
          rank() over(PARTITION BY customer_id
                      ORDER BY order_year) AS order_rnk
   FROM cte3)
SELECT customer_id
FROM cte4
EXCEPT
SELECT customer_id
FROM cte4
WHERE order_rnk!=price_rnk
```


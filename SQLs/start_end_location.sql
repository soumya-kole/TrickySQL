CREATE TABLE travel_data (
    customer VARCHAR(10),
    start_loc VARCHAR(50),
    end_loc VARCHAR(50)
);


INSERT INTO travel_data (customer, start_loc, end_loc) VALUES
    ('c1', 'New York', 'Lima'),
    ('c1', 'London', 'New York'),
    ('c1', 'Lima', 'Sao Paulo'),
    ('c1', 'Sao Paulo', 'New Delhi'),
    ('c2', 'Mumbai', 'Hyderabad'),
    ('c2', 'Surat', 'Pune'),
    ('c2', 'Hyderabad', 'Surat'),
    ('c3', 'Kochi', 'Kurnool'),
    ('c3', 'Lucknow', 'Agra'),
    ('c3', 'Agra', 'Jaipur'),
    ('c3', 'Jaipur', 'Kochi');

with cte as (
 select 
	coalesce (t1.customer,t2.customer) as customer,
	t1.start_loc as s1,
	t1.end_loc as e1,
	t2.start_loc as s2,
	t2.end_loc as e2
from travel_data t1 full outer join travel_data t2
on t1.customer = t2.customer
and t1.start_loc = t2.end_loc
where t1.start_loc is null or t2.end_loc is null)
select 
	customer,
	max(s1) as start_loc,
	max(e2) as end_loc
from cte	
group by 1
;
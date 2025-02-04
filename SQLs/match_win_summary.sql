## Objective
This is Leetcode problem [youtube](https://www.youtube.com/watch?v=qyAgWL066Vo&list=PLBTZqjSKn0IeKBQDjLmzisazhqQy4iGkb)


## Data preparation

```sql
create table icc_world_cup
(
Team_1 Varchar(20),
Team_2 Varchar(20),
Winner Varchar(20)
);
INSERT INTO icc_world_cup values('India','SL','India');
INSERT INTO icc_world_cup values('SL','Aus','Aus');
INSERT INTO icc_world_cup values('SA','Eng','Eng');
INSERT INTO icc_world_cup values('Eng','NZ','NZ');
INSERT INTO icc_world_cup values('Aus','India','India');

with all_matches as (
	select 
		Team_1 as team,
		case 
			when Team_1=Winner then 1
			else 0
		end as win_flag
	from icc_world_cup
	union all
	select 
		Team_2 as team,
		case 
			when Team_2=Winner then 1
			else 0
		end as win_flag
	from icc_world_cup
)
select 
	team,
	count(*) as total_matches,
	sum(win_flag) as no_of_win,
	count(*) - sum(win_flag) as no_of_loses
from all_matches
group by 1
order by 3 desc, total_matches
```


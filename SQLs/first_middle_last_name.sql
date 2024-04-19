create table customers  (customer_name varchar(30));
insert into customers values ('Soumya Kole')
,('Akash Kumar Singh')
,('Tom'); 

-- Postgress
SELECT split_part(customer_name,' ',1) as first_name
,case when split_part(customer_name,' ',3) ='' then  '' else split_part(customer_name,' ',2) end  as second_name
,case when split_part(customer_name,' ',3) ='' then  split_part(customer_name,' ',2)  else split_part(customer_name,' ',3)  end  as last_name
from 
    customers;

--MySQL
with t as (
SELECT
	customer_name, LENGTH (customer_name ) - LENGTH (REPLACE (customer_name,' ','')) as nos 
from customers c )
select 
	customer_name ,
	SUBSTRING_INDEX(customer_name,' ',1) as first_name,
    CASE 
        WHEN nos<2 THEN ''
        ELSE SUBSTRING_INDEX(SUBSTRING_INDEX(customer_name, ' ', 2),' ', -1)
    END AS second_name,
        CASE 
        WHEN nos = 0 THEN ''
        else SUBSTRING_INDEX(customer_name, ' ', -1)
    END AS last_name
from t ;


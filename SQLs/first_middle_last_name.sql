create table customers  (customer_name varchar(30));
insert into customers values ('Soumya Kole')
,('Akash Kumar Singh')
,('Tom'); 

SELECT split_part(customer_name,' ',1) as first_name
,case when split_part(customer_name,' ',3) ='' then  '' else split_part(customer_name,' ',2) end  as second_name
,case when split_part(customer_name,' ',3) ='' then  split_part(customer_name,' ',2)  else split_part(customer_name,' ',3)  end  as last_name
from 
    customers
# TRICKY SQL

This repository contains sample quetions, data and answer for Meta Data Engineering Interview https://www.metacareers.com/profile/preparation_hub?b=0121222&chooseView=SQL&p=DATA_ENG

## Prerequisite

Docker should be running in your system

## Environment

Clone the repository
Go to the Meta folder of the cloned repo
Execute following command 

```bash
docker compose up -d
```

Shutdown database using following command from same directory

```bash
docker compose down
```

## Connect Database

You can use any GUI tool like dBeaver.
Then connect the database using user/password as admin/admin
If you want to change user/password, use the docker-compose.yaml


## SQLS

1. [exchange seat](SQLs/exchange_seat.md)
2. [Customer with increasing purchase](SQLs/CustomerWithIncreasingPurchase.md)
3. [Hierarchical query in mysql](../SQLs/other_problems/connect-by-hierarchical-query/description.md)




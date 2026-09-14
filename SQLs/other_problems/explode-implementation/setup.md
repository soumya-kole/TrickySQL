# Explode Implementation - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS explode_table;

CREATE TABLE explode_table (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    csv_column VARCHAR(255)
);

INSERT INTO explode_table (csv_column) VALUES
    ('apple'),
    ('dog,cat,horse'),
    ('one,two,three,four');
```

Load this dataset:

```bash
make setup explode-implementation
```

/*
This is an SQL Only (no proc) implementation of Explode()
*/

-- Data preparation
CREATE DATABASE IF NOT EXISTS demo;
drop table demo.explode_table;
CREATE TABLE demo.explode_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    csv_column VARCHAR(255)
);

INSERT INTO demo.explode_table (csv_column) VALUES
    ('apple'),
    ('dog,cat,horse'),
    ('one,two,three,four');

select * from demo.explode_table;

-- Solution

WITH RECURSIVE CTE AS (
    SELECT
        id,
        SUBSTRING_INDEX(csv_column, ',', 1) AS value,
        SUBSTRING(csv_column, LENGTH(SUBSTRING_INDEX(csv_column, ',', 1)) + 2) AS remaining_values
    FROM demo.explode_table
    UNION ALL
    SELECT
        id,
        SUBSTRING_INDEX(remaining_values, ',', 1) AS value,
        SUBSTRING(remaining_values, LENGTH(SUBSTRING_INDEX(remaining_values, ',', 1)) + 2) AS remaining_values
    FROM CTE
    WHERE remaining_values <> ''
)
SELECT id, value
FROM CTE
ORDER BY id;

/*
Result will be like
1	apple
2	dog
2	cat
2	horse
3	one
3	two
3	three
3	four
*/
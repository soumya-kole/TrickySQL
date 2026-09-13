# Split Full Name into First/Middle/Last - Solutions

## Solution 1: `SUBSTRING_INDEX` keyed off word count

Count the words in `customer_name` from the number of spaces (`LENGTH(name) - LENGTH(REPLACE(name, ' ', ''))`). `first_name` is always the first word. For `second_name` and `last_name`, use `CASE` on the word count: with fewer than 2 words there's no second name, and with 0 or 1 words there's no last name; otherwise pull the word out with nested `SUBSTRING_INDEX` calls (positive `n` counts from the left, negative `n` counts from the right).

#### MySQL

```sql
WITH word_count AS (
    SELECT
        customer_name,
        LENGTH(customer_name) - LENGTH(REPLACE(customer_name, ' ', '')) AS spaces
    FROM customers
)
SELECT
    customer_name,
    SUBSTRING_INDEX(customer_name, ' ', 1) AS first_name,
    CASE
        WHEN spaces < 2 THEN ''
        ELSE SUBSTRING_INDEX(SUBSTRING_INDEX(customer_name, ' ', 2), ' ', -1)
    END AS second_name,
    CASE
        WHEN spaces = 0 THEN ''
        ELSE SUBSTRING_INDEX(customer_name, ' ', -1)
    END AS last_name
FROM word_count;
```

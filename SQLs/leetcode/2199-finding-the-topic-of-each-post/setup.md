# 2199. Finding the Topic of Each Post - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Keywords;

CREATE TABLE Keywords (
    topic_id INT,
    word     VARCHAR(50),
    PRIMARY KEY (topic_id, word)
);

CREATE TABLE Posts (
    post_id INT PRIMARY KEY,
    content VARCHAR(500)
);

INSERT INTO Keywords (topic_id, word) VALUES
(1, 'handball'),
(1, 'football'),
(3, 'WAR'),
(2, 'Vaccine');

INSERT INTO Posts (post_id, content) VALUES
(1, 'We call it soccer They call it football hahaha'),
(2, 'Americans prefer basketball while Europeans love handball and football'),
(3, 'stop the war and play handball'),
(4, 'warning I planted some flowers this morning and then got vaccinated');
```

Load this dataset:

```bash
make setup 2199-finding-the-topic-of-each-post
```

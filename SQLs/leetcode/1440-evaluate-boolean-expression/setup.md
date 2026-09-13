# 1440. Evaluate Boolean Expression - Setup

## Setup

```sql
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

DROP TABLE IF EXISTS Expressions;
DROP TABLE IF EXISTS Variables;

CREATE TABLE Variables (
    name  VARCHAR(5) PRIMARY KEY,
    value INT
);

CREATE TABLE Expressions (
    left_operand  VARCHAR(5),
    operator      ENUM('<', '>', '='),
    right_operand VARCHAR(5),
    PRIMARY KEY (left_operand, operator, right_operand)
);

INSERT INTO Variables (name, value) VALUES
('x', 66),
('y', 77);

INSERT INTO Expressions (left_operand, operator, right_operand) VALUES
('x', '>', 'y'),
('x', '<', 'y'),
('x', '=', 'y'),
('y', '>', 'x'),
('y', '<', 'x'),
('x', '=', 'x');
```

Load this dataset:

```bash
make setup 1440-evaluate-boolean-expression
```

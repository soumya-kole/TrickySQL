version: "3.8"
services:
  mssql:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: mssql_container
    ports:
      - "1433:1433"
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong!Password
    restart: on-failure:5  # Change restart policy



-- Create databases
CREATE DATABASE Database1;
CREATE DATABASE Database2;

-- Create User1 and assign to Database1
CREATE LOGIN User1 WITH PASSWORD = 'Ur1$AmfghY01!';
USE Database1;
CREATE USER User1 FOR LOGIN User1;
ALTER ROLE db_owner ADD MEMBER User1;

-- Create User2 and assign to Database2
CREATE LOGIN User2 WITH PASSWORD = 'Ur2$AmfghY01!';
USE Database2;
CREATE USER User2 FOR LOGIN User2;
ALTER ROLE db_owner ADD MEMBER User2;


USE Database1;
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,        -- Unique identifier for each employee
    FirstName NVARCHAR(50) NOT NULL,   -- Employee's first name
    LastName NVARCHAR(50) NOT NULL,    -- Employee's last name
    HireDate DATE,                     -- Date of hire
    Salary DECIMAL(18, 2)              -- Employee's salary
);

INSERT INTO Employees (EmployeeID, FirstName, LastName, HireDate, Salary)
VALUES
(1, 'John', 'Doe', '2023-01-01', 60000.00),
(2, 'Jane', 'Smith', '2023-02-01', 75000.00);

USE Database2;
CREATE TABLE Employees_2 (
    EmployeeID INT PRIMARY KEY,        -- Unique identifier for each employee
    FirstName NVARCHAR(50) NOT NULL,   -- Employee's first name
    LastName NVARCHAR(50) NOT NULL,    -- Employee's last name
    HireDate DATE,                     -- Date of hire
    Salary DECIMAL(18, 2)              -- Employee's salary
);
INSERT INTO Employees_2 (EmployeeID, FirstName, LastName, HireDate, Salary)
VALUES
(101, 'xxx', 'yyy', '2022-01-01', 60000.00),
(202, 'bbb', 'ccc', '2022-02-01', 75000.00);

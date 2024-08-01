
CREATE DATABASE employee_db;

CREATE TABLE employees (
   emp_id SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   skillset VARCHAR(100) NOT NULL,
   department VARCHAR(100),
   email VARCHAR(100),
   phone_number VARCHAR(15),
   address TEXT,
   date_of_joining DATE
);
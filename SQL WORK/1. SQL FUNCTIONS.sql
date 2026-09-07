--SELECT UPPER('data') FROM dual;

--SELECT UPPER('oracle sql') FROM dual;

--SELECT UPPER('hello world') FROM dual;

--SELECT first_name, UPPER(first_name) FROM hr.employees;

--SELECT last_name, UPPER(last_name) FROM hr.employees;

--SELECT employee_id, first_name, last_name FROM hr.employees WHERE UPPER(first_name) = 'STEVEN';

--SELECT LOWER('ORACLE') FROM dual;

--SELECT LOWER('ORACLE SQL PROGRAMMING') FROM dual;

/*
SELECT first_name,
           LOWER(first_name)
    FROM hr.employees;
*/

/*
SELECT email,
           LOWER(email)
    FROM hr.employees;
*/

/*
SELECT employee_id,
           first_name,
           email
    FROM hr.employees
    WHERE LOWER(email) = 'sking';
*/

--SELECT INITCAP('oracle sql programming') FROM dual;

--SELECT INITCAP('HELLO WORLD') FROM dual;

--SELECT INITCAP('data science and machine learning') FROM dual;

/*
SELECT first_name,
           INITCAP(first_name)
    FROM hr.employees;
*/

--SELECT INITCAP(first_name || ' ' || last_name) AS full_name FROM hr.employees;

--SELECT LENGTH('oracle') FROM dual;

--SELECT LENGTH('data science') FROM dual;

/*
SELECT first_name,
           LENGTH(first_name)
    FROM hr.employees;
*/

/*
SELECT employee_id,
           first_name,
           LENGTH(first_name)
    FROM hr.employees
    WHERE LENGTH(first_name) > 6;
*/

/*
SELECT employee_id,
           last_name
    FROM hr.employees
    WHERE LENGTH(last_name) = 5;
*/

--SELECT SUBSTR('oracle',1,3) FROM dual;

--SELECT SUBSTR('oracle',2,3) FROM dual;

--SELECT SUBSTR('oracle',3,2) FROM dual;

--SELECT SUBSTR('oracle',3) FROM dual;

--SELECT SUBSTR('oracle',-3) FROM dual;

--SELECT SUBSTR('oracle',-2) FROM dual;

/*
SELECT first_name,
           SUBSTR(first_name,1,3)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,1,1)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,-3)
    FROM hr.employees;
*/
/*
SELECT email,
           SUBSTR(email,1,3)
    FROM hr.employees;
*/

--SELECT CONCAT('oracle','programming') FROM dual;

--SELECT CONCAT('oracle ','programming') FROM dual;

/*
SELECT first_name,
           last_name,
           CONCAT(first_name,last_name)
    FROM hr.employees;
*/

--SELECT CONCAT(first_name, CONCAT(' ',last_name)) AS full_name FROM hr.employees;

--SELECT first_name || ' ' || last_name AS full_name FROM hr.employees;

--SELECT employee_id || ' - ' || first_name || ' ' || last_name FROM hr.employees;

--SELECT REPLACE('hello world','world','oracle') FROM dual;

--SELECT REPLACE('oracle database','database','sql') FROM dual;

--SELECT REPLACE('123-456-789','-','') FROM dual;

--SELECT REPLACE('oracle sql developer',' ','_') FROM dual;

/*
SELECT first_name,
           REPLACE(first_name,'a','@')
    FROM hr.employees;
*/

/*
SELECT email,
           REPLACE(email,'A','@')
    FROM hr.employees;
*/

--SELECT TRIM('   oracle   ') FROM dual;

/*
SELECT first_name,
           TRIM(first_name)
    FROM hr.employees;
*/

/*
SELECT *
    FROM hr.employees
    WHERE TRIM(first_name) = 'Steven';
*/

--SELECT TRIM('  oracle sql  ') FROM dual;

--SELECT LTRIM('   oracle') FROM dual;

--SELECT LTRIM('****oracle','*') FROM dual;

--SELECT LTRIM('000123','0') FROM dual;

--SELECT LTRIM('AAAOracle','A') FROM dual;

/*
SELECT first_name,
           LTRIM(first_name)
    FROM hr.employees;
*/

--SELECT RTRIM('oracle   ') FROM dual;

--SELECT RTRIM('1230000','0') FROM dual;

--SELECT RTRIM('oracle****','*') FROM dual;

--SELECT RTRIM('OracleAAA','A') FROM dual;

/*
SELECT first_name,
           RTRIM(first_name)
    FROM hr.employees;
*/

--SELECT TRIM('   oracle   ') FROM dual;

--SELECT LTRIM('***oracle','*') FROM dual;

--SELECT RTRIM('oracle***','*') FROM dual;

--SELECT LPAD('123',5,'0') FROM dual;

--SELECT LPAD('oracle',7,'_') FROM dual;

--SELECT LPAD('100',8,'0') FROM dual;

--SELECT LPAD('SQL',10,'*') FROM dual;

--SELECT LPAD('123',10,'AB') FROM dual;

/*
SELECT employee_id,
           LPAD(employee_id,6,'0') AS formatted_employee_id
    FROM hr.employees;
*/

/*
SELECT salary,
           LPAD(salary,10,'*')
    FROM hr.employees;
*/

--SELECT LPAD('ORACLE',4,'0') FROM dual;

--SELECT RPAD('oracle',10,'*') FROM dual;

--SELECT RPAD('123',5,'0') FROM dual;

--SELECT RPAD('SQL',10,'.') FROM dual;

/*
SELECT first_name,
           RPAD(first_name,15,'.')
    FROM hr.employees;
*/

--SELECT RPAD('ORACLE',4,'*') FROM dual;

/*
SELECT LPAD('123',5,'0'),
           RPAD('123',5,'0')
    FROM dual;
*/

--SELECT ASCII('A') FROM dual;

--SELECT ASCII('B') FROM dual;

--SELECT ASCII('C') FROM dual;

--SELECT ASCII('a') FROM dual;

--SELECT ASCII('0') FROM dual;

--SELECT ASCII('ABC') FROM dual;

/*
SELECT first_name,
           ASCII(first_name)
    FROM hr.employees;
*/

--SELECT CHR(65) FROM dual;

--SELECT CHR(66) FROM dual;

--SELECT CHR(67) FROM dual;

--SELECT CHR(97) FROM dual;

--SELECT CEIL(10.9) FROM dual;

--SELECT CEIL(10) FROM dual;

--SELECT CEIL(15.01) FROM dual;

--SELECT CEIL(99.99) FROM dual;

/*
SELECT salary,
           salary / 12,
           CEIL(salary / 12)
    FROM hr.employees;
*/

--SELECT FLOOR(10.1) FROM dual;

--SELECT FLOOR(10.9) FROM dual;

--SELECT FLOOR(10) FROM dual;

--SELECT FLOOR(15.99) FROM dual;

--SELECT FLOOR(99.01) FROM dual;

/*
SELECT salary,
           salary / 12,
           FLOOR(salary / 12)
    FROM hr.employees;
*/

/*
SELECT CEIL(10.7),
           FLOOR(10.7)
    FROM dual;
*/

--SELECT MOD(10,3) FROM dual;

--SELECT MOD(20,5) FROM dual;

--SELECT MOD(11,2) FROM dual;

--SELECT MOD(10,2) FROM dual;

--SELECT MOD(11,2) FROM dual;

/*
SELECT employee_id,
           first_name
    FROM hr.employees
    WHERE MOD(employee_id,2) = 0;
*/

/*
SELECT employee_id,
           first_name
    FROM hr.employees
    WHERE MOD(employee_id,2) = 1;
*/

/*
SELECT employee_id,
           MOD(employee_id,10)
    FROM hr.employees;
*/

--SELECT ABS(-10.3) FROM dual;

--SELECT ABS(-100) FROM dual;

--SELECT ABS(100) FROM dual;

--SELECT ABS(0) FROM dual;

/*
SELECT employee_id,
           salary,
           ABS(salary - 10000) AS salary_difference
    FROM hr.employees;
*/

--SELECT POWER(2,3) FROM dual;

--SELECT POWER(5,2) FROM dual;

--SELECT POWER(10,3) FROM dual;

--SELECT POWER(10,0) FROM dual;

--SELECT POWER(2,0.5) FROM dual;

--SELECT POWER(16,0.5) FROM dual;

--SELECT POWER(2,1/2) FROM dual;

--SELECT POWER(2,0.5) FROM dual;

--SELECT POWER(3,3) FROM dual;

/*
SELECT employee_id,
           salary,
           POWER(salary,2)
    FROM hr.employees;
*/

--SELECT SQRT(16) FROM dual;

--SELECT SQRT(25) FROM dual;

--SELECT SQRT(2) FROM dual;

--SELECT SQRT(100) FROM dual;

/*
SELECT employee_id,
           salary,
           SQRT(salary)
    FROM hr.employees;
*/

/*
SELECT SQRT(16),
           POWER(16,0.5),
           POWER(16,1/2)
    FROM dual;
*/

-- COMPLETE CHARACTER FUNCTION PRACTICE USING DUAL

--SELECT UPPER('oracle') FROM dual;

--SELECT LOWER('ORACLE') FROM dual;

--SELECT INITCAP('oracle sql programming') FROM dual;

--SELECT LENGTH('oracle') FROM dual;

--SELECT LENGTH('data science') FROM dual;

--SELECT SUBSTR('oracle',1,3) FROM dual;

--SELECT SUBSTR('oracle',2,3) FROM dual;

--SELECT SUBSTR('oracle',3) FROM dual;

--SELECT SUBSTR('oracle',-3) FROM dual;

--SELECT CONCAT('oracle','programming') FROM dual;

--SELECT CONCAT('oracle ','programming') FROM dual;

--SELECT REPLACE('hello world','world','oracle') FROM dual;

--SELECT REPLACE('123-456-789','-','') FROM dual;

--SELECT TRIM('   oracle   ') FROM dual;

--SELECT LTRIM('   oracle') FROM dual;

--SELECT LTRIM('****oracle','*') FROM dual;

--SELECT RTRIM('1230000','0') FROM dual;

--SELECT LPAD('123',5,'0') FROM dual;

--SELECT RTRIM('1230000','0') FROM dual;

--SELECT LPAD('123',5,'0') FROM dual;

--SELECT LPAD('oracle',7,'_') FROM dual;

--SELECT RPAD('123',5,'0') FROM dual;

--SELECT RPAD('oracle',10,'*') FROM dual;

--SELECT ASCII('A') FROM dual;

--SELECT CHR(65) FROM dual;

-- COMPLETE CHARACTER FUNCTION PRACTICE USING HR.EMPLOYEES

/*
SELECT first_name,
           UPPER(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           LOWER(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           INITCAP(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           LENGTH(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,1,3)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,1,1)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,-3)
    FROM hr.employees;
*/

/*
SELECT first_name,
           last_name,
           CONCAT(first_name,last_name)
    FROM hr.employees;
*/

--SELECT first_name || ' ' || last_name AS full_name FROM hr.employees;

/*
SELECT first_name,
           REPLACE(first_name,'a','@')
    FROM hr.employees;
*/

/*
SELECT first_name,
           TRIM(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           LTRIM(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           RTRIM(first_name)
    FROM hr.employees;
*/

/*
SELECT employee_id,
           LPAD(employee_id,6,'0')
    FROM hr.employees;
*/

/*
SELECT first_name,
           RPAD(first_name,15,'.')
    FROM hr.employees;
*/

/*
SELECT first_name,
           ASCII(first_name)
    FROM hr.employees;
*/

-- COMPLETE NUMERIC FUNCTION PRACTICE USING DUAL

--SELECT CEIL(10.1) FROM dual;

--SELECT CEIL(10.9) FROM dual;

--SELECT CEIL(10) FROM dual;

--SELECT CEIL(99.01) FROM dual;

--SELECT FLOOR(10.1) FROM dual;

--SELECT FLOOR(10.9) FROM dual;

--SELECT FLOOR(10) FROM dual;

--SELECT FLOOR(99.99) FROM dual;

--SELECT MOD(10,3) FROM dual;

--SELECT MOD(20,5) FROM dual;

--SELECT MOD(11,2) FROM dual;

--SELECT MOD(100,7) FROM dual;

--SELECT ABS(-10.3) FROM dual;

--SELECT ABS(-100) FROM dual;

--SELECT ABS(0) FROM dual;

--SELECT POWER(2,3) FROM dual;

--SELECT POWER(5,2) FROM dual;

--SELECT POWER(10,3) FROM dual;

--SELECT POWER(2,0.5) FROM dual;

--SELECT POWER(2,1/2) FROM dual;

--SELECT SQRT(2) FROM dual;

--SELECT SQRT(16) FROM dual;

--SELECT SQRT(25) FROM dual;

--SELECT SQRT(100) FROM dual;

-- COMPLETE NUMERIC FUNCTION PRACTICE USING HR.EMPLOYEES

/*
SELECT employee_id,
           salary,
           salary / 12 AS divided_salary,
           CEIL(salary / 12) AS ceil_value
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           salary / 12 AS divided_salary,
           FLOOR(salary / 12) AS floor_value
    FROM hr.employees;
*/

/*
SELECT employee_id,
           MOD(employee_id,2) AS remainder
    FROM hr.employees;
*/

/*
SELECT employee_id,
           first_name
    FROM hr.employees
    WHERE MOD(employee_id,2) = 0;
*/

/*
SELECT employee_id,
           first_name
    FROM hr.employees
    WHERE MOD(employee_id,2) = 1;
*/

/*
SELECT employee_id,
           salary,
           ABS(salary - 10000) AS salary_difference
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           POWER(salary,2) AS salary_square
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           SQRT(salary) AS salary_square_root
    FROM hr.employees;
*/

-- FINAL PRACTICE SET

--SELECT UPPER('data engineering') FROM dual;

--SELECT LOWER('DATA ENGINEERING') FROM dual;

--SELECT INITCAP('oracle database administrator') FROM dual;

--SELECT LENGTH('machine learning') FROM dual;

--SELECT SUBSTR('artificial intelligence',1,10) FROM dual;

--SELECT CONCAT('Oracle ','SQL') FROM dual;

--SELECT REPLACE('hello python','python','oracle') FROM dual;

--SELECT TRIM('    database    ') FROM dual;

--SELECT LTRIM('00000500','0') FROM dual;

--SELECT RTRIM('500000','0') FROM dual;

--SELECT LPAD('500',8,'0') FROM dual;

--SELECT RPAD('SQL',10,'.') FROM dual;

--SELECT ASCII('A') FROM dual;

--SELECT CHR(65) FROM dual;

--SELECT CEIL(25.01) FROM dual;

--SELECT FLOOR(25.99) FROM dual;

--SELECT MOD(25,4) FROM dual;

--SELECT ABS(-999.50) FROM dual;

--SELECT POWER(3,4) FROM dual;

--SELECT SQRT(81) FROM dual;

/*
SELECT first_name,
           UPPER(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           LOWER(first_name)
    FROM hr.employees;
*/

/*
 SELECT first_name,
           INITCAP(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           LENGTH(first_name)
    FROM hr.employees;
*/

/*
SELECT first_name,
           SUBSTR(first_name,1,3)
    FROM hr.employees;
*/

--SELECT first_name || ' ' || last_name AS full_name FROM hr.employees;

/*
SELECT employee_id,
       LPAD(employee_id,6,'0') AS formatted_id
FROM hr.employees;
*/

/*
SELECT first_name,
           RPAD(first_name,20,'.') AS formatted_name
    FROM hr.employees;
*/

/*
 SELECT employee_id,
           salary,
           CEIL(salary / 12) AS ceil_monthly_salary
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           FLOOR(salary / 12) AS floor_monthly_salary
    FROM hr.employees;
*/

/*
SELECT employee_id,
           MOD(employee_id,2) AS remainder
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           ABS(salary - 10000) AS difference_from_10000
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           POWER(salary,2) AS salary_square
    FROM hr.employees;
*/

/*
SELECT employee_id,
           salary,
           SQRT(salary) AS salary_square_root
    FROM hr.employees;
*/
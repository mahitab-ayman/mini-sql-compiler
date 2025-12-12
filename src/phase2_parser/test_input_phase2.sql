-- ============================================
-- PHASE 2 TEST SUITE - SYNTAX ANALYSIS
-- ============================================

-- ============================================
-- VALID QUERIES - All should parse successfully
-- ============================================

-- Test 1: Simple SELECT
SELECT * FROM Students;

-- Test 2: SELECT with column list
SELECT name, age, email FROM Students;

-- Test 3: SELECT with WHERE clause
SELECT * FROM Students WHERE age > 18;

-- Test 4: SELECT with compound condition (AND)
SELECT * FROM Students WHERE age > 18 AND status = 'active';

-- Test 5: SELECT with compound condition (OR)
SELECT * FROM Students WHERE age > 18 OR status = 'active';

-- Test 6: SELECT with NOT condition
SELECT * FROM Students WHERE NOT discontinued;

-- Test 7: SELECT with complex condition
SELECT * FROM Students WHERE (age > 18 AND age < 25) OR status = 'active';

-- Test 8: SELECT with arithmetic expressions
SELECT name, age + 1, salary * 1.1 FROM Employees;

-- Test 9: INSERT statement
INSERT INTO Users VALUES (1, 'John', 'john@example.com');

-- Test 10: INSERT with expressions
INSERT INTO Products VALUES (1, 'Product', 10.5 * 2);

-- Test 11: UPDATE statement
UPDATE Users SET name = 'Jane' WHERE id = 1;

-- Test 12: UPDATE with multiple assignments
UPDATE Users SET name = 'Jane', email = 'jane@example.com' WHERE id = 1;

-- Test 13: DELETE statement
DELETE FROM Users WHERE id = 1;

-- Test 14: DELETE without WHERE
DELETE FROM Users;

-- Test 15: CREATE TABLE statement
CREATE TABLE Students (id INT, name TEXT, gpa FLOAT);

-- Test 16: Multiple statements
SELECT * FROM Users;
INSERT INTO Users VALUES (1, 'Test');
UPDATE Users SET name = 'Updated' WHERE id = 1;

-- ============================================
-- INVALID QUERIES - Should produce syntax errors
-- ============================================

-- Error 1: Missing FROM keyword
SELECT name Students;

-- Error 2: Missing table name
SELECT * FROM;

-- Error 3: Missing closing parenthesis in INSERT
INSERT INTO Users VALUES (1, 'John';

-- Error 4: Missing VALUES keyword
INSERT INTO Users (1, 'John');

-- Error 5: Missing SET keyword in UPDATE
UPDATE Users name = 'Jane' WHERE id = 1;

-- Error 6: Missing condition after WHERE
SELECT * FROM Students WHERE;

-- Error 7: Missing operator in comparison
SELECT * FROM Students WHERE age 18;

-- Error 8: Missing closing parenthesis in condition
SELECT * FROM Students WHERE (age > 18;

-- Error 9: Missing data type in CREATE TABLE
CREATE TABLE Students (id, name TEXT);

-- Error 10: Missing comma in column list
SELECT name age FROM Students;

-- Error 11: Unexpected token
SELECT * FROM Students WHERE age > 18 AND;

-- Error 12: Missing table name in DELETE
DELETE FROM;

-- ============================================
-- COMPLEX VALID QUERIES
-- ============================================

-- Complex SELECT with all features
SELECT 
    student_id, 
    full_name, 
    (score + bonus) AS total_score
FROM students 
WHERE gpa > 3.5 
AND (age > 18 AND age < 25)
OR status = 'active';

-- Multiple CREATE and INSERT
CREATE TABLE Products (id INT, name TEXT, price FLOAT);
INSERT INTO Products VALUES (1, 'Product1', 10.99);
INSERT INTO Products VALUES (2, 'Product2', 20.50);

-- Complex UPDATE with arithmetic
UPDATE Products SET price = price * 1.1 WHERE price < 100;

-- Complex DELETE with compound condition
DELETE FROM Products WHERE price < 10 OR discontinued = 1;


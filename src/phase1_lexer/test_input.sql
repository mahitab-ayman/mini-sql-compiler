-- ============================================
-- PHASE 1 TEST SUITE - COMPREHENSIVE TESTS
-- ============================================

-- ============================================
-- TEST 1: All Keywords (Case-Sensitive)
-- ============================================
SELECT * FROM Students;
select name from courses;
Select id From users;
sELeCt email FrOm contacts;

CREATE TABLE Users (id INT, name TEXT);
INSERT INTO Users VALUES (1, 'Ahmed');
UPDATE Users SET name = 'Ali' WHERE id = 1;
DELETE FROM Users WHERE id = 1;

WHERE age > 18 AND status = 'active';
SELECT * FROM Products WHERE price > 100 OR discount < 0.5;

-- ============================================
-- TEST 2: Identifiers (Start with letter, contain digits/underscores)
-- ============================================
SELECT student_id, full_name, email_address FROM students;
SELECT _private, data_2024, col1, COL_2 FROM table_name;
INSERT INTO user_accounts VALUES (1, 'test');

-- ============================================
-- TEST 3: String Literals (Single Quotes)
-- ============================================
INSERT INTO Students VALUES (1, 'Nada Zaki', 'n.zaki@nu.edu.eg');
INSERT INTO Students VALUES (2, 'Ahmed Ali', 'ahmed@nu.edu.eg');
SELECT * FROM Students WHERE email = 'nada@example.com';
UPDATE Students SET full_name = 'Nada Gamal Zaki' WHERE id = 1;

-- ============================================
-- TEST 4: Numeric Literals (Integers and Floats)
-- ============================================
SELECT 100, 200, 500 FROM numbers;
SELECT 3.14, 2.5, 99.99 FROM decimals;
SELECT id + 10, price * 1.5 FROM products;
SELECT score - 5, salary / 12 FROM employees;

-- ============================================
-- TEST 5: Arithmetic Operators
-- ============================================
SELECT salary + bonus FROM employees;
SELECT total - discount FROM orders;
SELECT quantity * price FROM items;
SELECT amount / count FROM statistics;
SELECT value % 2 FROM numbers;

-- ============================================
-- TEST 6: Comparison Operators
-- ============================================
SELECT * FROM students WHERE age > 20;
SELECT * FROM employees WHERE salary < 5000;
SELECT * FROM products WHERE price = 100;
SELECT * FROM users WHERE status != 'inactive';
SELECT * FROM items WHERE value <> 0;
SELECT * FROM records WHERE score >= 80;
SELECT * FROM data WHERE value <= 100;

-- ============================================
-- TEST 7: Logical Operators (AND, OR, NOT)
-- ============================================
SELECT * FROM Students WHERE age > 18 AND age < 25;
SELECT * FROM Users WHERE status = 'active' OR role = 'admin';
SELECT * FROM Products WHERE NOT discontinued;

-- ============================================
-- TEST 8: Delimiters and Punctuation
-- ============================================
SELECT (id + 10) FROM users;
SELECT a, b, c, d FROM table1;
INSERT INTO Students VALUES (1, 'Ali', 'ali@nu.edu.eg');
SELECT * FROM Students;

-- ============================================
-- TEST 9: Single-Line Comments (--)
-- ============================================
-- This is a single-line comment
SELECT * FROM Students;  -- Fetch all students
-- Another comment
SELECT id, name FROM users;  -- Get user info

-- ============================================
-- TEST 10: Multi-Line Comments (#...#)
-- ============================================
# This is a multi-line comment
that spans across multiple lines
and continues until it closes #
SELECT * FROM courses;

# Another multi-line comment
explaining the query #
SELECT name FROM students;

-- ============================================
-- TEST 11: Whitespace Handling
-- ============================================
SELECT    *     FROM     students;
SELECT
    id,
    name,
    email
FROM
    users;

-- ============================================
-- TEST 12: ERROR - Invalid Character (@)
-- ============================================
SELECT @id FROM students;
UPDATE users SET email = user@domain.com WHERE id = 1;

-- ============================================
-- TEST 13: ERROR - Unclosed String Literal
-- ============================================
INSERT INTO students VALUES (3, 'Ahmed', 'ahmed@nu.edu.eg;

-- ============================================
-- TEST 14: ERROR - Unterminated Multi-Line Comment
-- ============================================
# This comment is not closed
SELECT * FROM students;

-- ============================================
-- TEST 15: Complex Query with All Token Types
-- ============================================
SELECT 
    student_id, 
    full_name, 
    gpa,
    (score + bonus) AS total_score
FROM students 
WHERE gpa > 3.5 
AND (age > 18 AND age < 25)
OR status = 'active'
ORDER BY gpa DESC;

-- ============================================
-- TEST 16: Data Types
-- ============================================
CREATE TABLE Students (
    id INT,
    name TEXT,
    score FLOAT
);

-- ============================================
-- TEST 17: Mixed Keywords and Identifiers
-- ============================================
SELECT COUNT FROM stats;
SELECT FROM FROM tables;
SELECT INTO FROM destinations;
SELECT VALUES FROM records;

-- ============================================
-- TEST 18: Edge Cases
-- ============================================
SELECT _ FROM t;
SELECT _1 FROM t1;
SELECT a_b_c_d FROM table_with_underscores;
SELECT 0, 0.0, 1.0 FROM numbers;

-- ============================================
-- TEST 19: All Keywords Together
-- ============================================
SELECT col1, col2 FROM Table1 WHERE id > 10 INSERT INTO Table2 VALUES (1, 2);
UPDATE Table1 SET col1 = 'new' WHERE id = 1;
DELETE FROM Table1 WHERE id = 1;
CREATE TABLE Test (id INT, name TEXT);

-- ============================================
-- TEST 20: Case Sensitivity Mixed
-- ============================================
select Name, EMAIL from students where Age > 20;
Select ID, Price From Products Where Stock <= 10;
SELECT id, price FROM products WHERE stock <= 10;

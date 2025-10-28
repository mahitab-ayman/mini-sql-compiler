-- SQL Test Input for Nile University Students

## Creating the table for 
Nile University students
#

CREATE TABLE Students (
    student_id INT,
    full_name TEXT,
    email TEXT
);

-- Inserting student data
INSERT INTO Students VALUES (221000829, 'Nada Zaki', 'n.gamal2229@nu.edu.eg');
INSERT INTO Students VALUES (221000415, 'Mona Elsayed', 'm.gomaa2215@nu.edu.eg');
INSERT INTO Students VALUES (212002434, 'Mahitab Ayman', 'm.ayman2134@nu.edu.eg');

-- Selecting all data
SELECT * FROM Students;

-- Selecting specific columns
SELECT full_name, email FROM Students;

-- Filtering results
SELECT full_name FROM Students WHERE student_id > 221000400 AND student_id < 221000830;

-- Testing operators and expressions
SELECT student_id + 1000 AS new_id, full_name FROM Students WHERE student_id <> 212002434;

-- Updating data
UPDATE Students
SET full_name = 'Nada Gamal Zaki'
WHERE student_id = 221000829;

-- Deleting a student
DELETE FROM Students WHERE student_id = 212002434;

-- Mixed-case keywords and identifiers
select Full_Name, Email from students where Student_ID = 221000415;

-- Testing string literal error
INSERT INTO Students VALUES (221000999, 'Unclosed String, 'fake@nu.edu.eg');

-- Final comment
-- realistic Nile University data and all lexical elements.

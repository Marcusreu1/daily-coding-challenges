-- 1075. Project Employees I
-- Difficulty: Easy
-- https://leetcode.com/problems/project-employees-i/

/*
PROBLEM:
Calculate the average years of experience of employees for each project.
Round to 2 decimal places.

TABLES:
- Project (project_id, employee_id)
- Employee (employee_id, name, experience_years)

EXPECTED OUTPUT:
| project_id | average_years |
|------------|---------------|
| 1          | 2.00          |
| 2          | 2.50          |
*/

-- STEP 1: LEFT JOIN to connect projects with employees
-- Use LEFT JOIN because I want ALL projects (even if they have no employees)
-- ON: Connect when employee_id matches in both tables

-- STEP 2: AVG() to calculate the average of experience_years
-- AVG() sums all values and divides by the count automatically
-- No need for SUM()/COUNT() because it's a simple average (not weighted)

-- STEP 3: ROUND(..., 2) to round to 2 decimal places
-- The problem specifically requires 2 decimals

-- STEP 4: GROUP BY project_id
-- Need to group because I want ONE average PER project
-- Without GROUP BY, it would give me a single average of ALL employees

SELECT 
    p.project_id,                        -- Column to identify the project
    ROUND(                               -- Round to 2 decimal places
        AVG(e.experience_years),         -- Average of years of experience
        2
    ) AS average_years                   -- Alias for the result column
FROM Project p                           -- Main table: projects
LEFT JOIN Employee e                     -- Bring employee info (LEFT = include all projects)
    ON p.employee_id = e.employee_id     -- Condition: same employee_id
GROUP BY p.project_id;                   -- Group by project (one result per project)

/*
WHY EACH PART:
- LEFT JOIN: If there are projects without employees, they still appear (with NULL)
- AVG(): Simpler than SUM()/COUNT() for basic averages
- ROUND(value, 2): Format required by the problem
- GROUP BY: Without this, it would give ONE total average (incorrect)

CONCEPTS USED:
- LEFT JOIN
- AVG() aggregate function
- ROUND()
- GROUP BY

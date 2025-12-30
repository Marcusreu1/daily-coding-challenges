-- 185. Department Top Three Salaries
-- Difficulty: Hard
-- https://leetcode.com/problems/department-top-three-salaries/

/*
PROBLEM:
Find employees who rank in the top 3 unique salaries in their department.
An employee is in the top 3 if there are no more than 3 distinct salaries higher than theirs in the same department.

TABLES:
- Employee (id PK, name, salary, departmentId)
- Department (id PK, name)

EXPECTED OUTPUT:
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+

EXAMPLE:
IT Department unique salaries (ranked):
  1. 90000 (Max)
  2. 85000 (Joe, Randy) -- Tie, both rank 2
  3. 70000 (Will)
  4. 69000 (Janet) -- Rank 4, excluded

Sales Department unique salaries (ranked):
  1. 80000 (Henry)
  2. 60000 (Sam)
  
Top 3 includes all employees with salary ranks 1, 2, or 3 within their department.
*/

-- STEP 1: Subquery assigns rank to each employee within their department
-- DENSE_RANK() ensures no gaps in ranking (1,2,2,3 not 1,2,2,4)
-- PARTITION BY departmentId resets ranking for each department
-- ORDER BY salary DESC ranks highest salaries first

-- STEP 2: JOIN with Department table to get department names
-- Connects departmentId to department name for output

-- STEP 3: Filter for top 3 ranks only
-- WHERE salary_rank <= 3 includes all employees in top 3 unique salaries

SELECT 
    d.name AS Department, 
    e.name AS Employee, 
    e.salary AS Salary
FROM (
    SELECT 
        name, 
        salary, 
        departmentId,
        DENSE_RANK() OVER (                                                      -- Assign rank within each department
            PARTITION BY departmentId                                            -- Separate ranking per department
            ORDER BY salary DESC                                                 -- Highest salary gets rank 1
        ) AS salary_rank
    FROM Employee
) e
JOIN Department d ON e.departmentId = d.id                                       -- Get department name
WHERE salary_rank <= 3;                                                          -- Filter top 3 unique salaries

/*
WHY EACH PART:
- DENSE_RANK(): Ranks without gaps (1,2,2,3 not 1,2,2,4) for "top N distinct values"
- PARTITION BY departmentId: Creates separate ranking for each department
- ORDER BY salary DESC: Highest salaries get lower rank numbers (1 is best)
- Subquery: Calculates ranks before filtering (window functions can't be in WHERE directly)
- JOIN Department: Connects employee data to department name for output
- WHERE salary_rank <= 3: Filters employees in top 3 salary tiers per department
- Column aliases: Matches expected output format (Department, Employee, Salary)

WHY DENSE_RANK (not RANK or ROW_NUMBER):
- DENSE_RANK(): Top 3 means 3 DISTINCT salary values (1,2,2,3) ✓
- RANK(): Would skip numbers after ties (1,2,2,4) - rank 3 would be missing ✗
- ROW_NUMBER(): Would arbitrarily break ties (1,2,3,4) - excludes tied employees ✗

Example with different functions:
Salaries: 90000, 85000, 85000, 70000, 69000

DENSE_RANK: 1, 2, 2, 3, 4 → Top 3 includes 90k, 85k, 70k ✓
RANK:       1, 2, 2, 4, 5 → Top 3 would only include 90k, 85k ✗
ROW_NUMBER: 1, 2, 3, 4, 5 → Top 3 excludes one person with 85k ✗

WHY PARTITION BY:
- Resets ranking for each department independently
- IT department rankings: 1, 2, 2, 3, 4
- Sales department rankings: 1, 2 (starts over at 1)
- Without PARTITION BY: Rankings would be across all departments (wrong)

KEY TECHNIQUE:
- DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...): Rank within groups
- Subquery pattern: Calculate window function, then filter by rank
- Window functions cannot be used directly in WHERE clause

ALTERNATIVE APPROACH (correlated subquery):
SELECT 
    d.name AS Department,
    e1.name AS Employee,
    e1.salary AS Salary
FROM Employee e1
JOIN Department d ON e1.departmentId = d.id
WHERE 3 > (
    SELECT COUNT(DISTINCT e2.salary)
    FROM Employee e2
    WHERE e2.departmentId = e1.departmentId
    AND e2.salary > e1.salary
);

-- Counts how many DISTINCT salaries are higher than current employee
-- If less than 3, employee is in top 3
-- Less efficient than window functions for large datasets

EDGE CASES:
- Department with < 3 employees: All included (rank <= 3 always true)
- Multiple employees with same salary: All included (ties handled by DENSE_RANK)
- Department with only 1 unique salary: All employees rank 1 (all included)
- Employee in non-existent department: Excluded by INNER JOIN
- Multiple ties at 3rd position: All included (DENSE_RANK assigns same rank)

CONCEPTS USED:
- Window functions: DENSE_RANK() OVER
- PARTITION BY (ranking within groups)
- ORDER BY within window function
- Subquery in FROM clause (derived table)
- INNER JOIN
- WHERE with window function result
- Column aliasing
*/

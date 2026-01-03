-- 176. Second Highest Salary
-- Difficulty: Medium
-- https://leetcode.com/problems/second-highest-salary/

/*
PROBLEM:
Find the second highest salary from the Employee table.
If there is no second highest salary, return NULL.
The result column should be named SecondHighestSalary.

TABLES:
- Employee (id PK, salary)

EXPECTED OUTPUT:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+

EXAMPLE 1 (with second highest):
Input: Salaries [100, 200, 300]
Distinct salaries DESC: [300, 200, 100]
Second value: 200 ✓

EXAMPLE 2 (without second highest):
Input: Salaries [100]
Distinct salaries DESC: [100]
Second value: (doesn't exist) → NULL ✓

EXAMPLE 3 (with duplicate highest):
Input: Salaries [100, 200, 200]
Distinct salaries DESC: [200, 100]
Second value: 100 ✓
*/

-- STEP 1: Subquery finds distinct salaries in descending order
-- DISTINCT removes duplicate salary values
-- ORDER BY salary DESC sorts from highest to lowest
-- LIMIT 1 OFFSET 1 skips first (highest) and takes second

-- STEP 2: Outer SELECT handles NULL case
-- If subquery returns no result, outer SELECT returns NULL automatically
-- Column alias SecondHighestSalary names the result

SELECT 
    (SELECT DISTINCT salary                                                      -- Get unique salary values
     FROM Employee
     ORDER BY salary DESC                                                        -- Highest to lowest
     LIMIT 1 OFFSET 1)                                                           -- Skip 1st, take 2nd
    AS SecondHighestSalary;                                                      -- Name the result column

/*
WHY EACH PART:
- DISTINCT: Eliminates duplicate salaries (treats 200,200 as single value)
- ORDER BY salary DESC: Sorts from highest to lowest salary
- LIMIT 1: Returns only one row (the second highest)
- OFFSET 1: Skips the first row (highest salary)
- Outer SELECT: Converts empty result to NULL automatically
- Subquery in SELECT: Returns single value or NULL (scalar subquery)
- AS SecondHighestSalary: Names the output column as required

HOW OFFSET WORKS:
Distinct salaries: [300, 200, 100]
OFFSET 0: 300 (default, first row)
OFFSET 1: 200 (skip first, take second) ✓
OFFSET 2: 100 (skip two, take third)

WHY DISTINCT IS CRITICAL:
Without DISTINCT:
Salaries: [200, 200, 100]
ORDER BY DESC: [200, 200, 100]
OFFSET 1: 200 (still highest, wrong!) ✗

With DISTINCT:
Salaries: [200, 200, 100]
DISTINCT + ORDER BY DESC: [200, 100]
OFFSET 1: 100 (second highest, correct!) ✓

WHY OUTER SELECT (not just IFNULL):
- Subquery in SELECT clause automatically returns NULL if empty
- More elegant than wrapping with IFNULL
- IFNULL would be redundant: IFNULL((subquery), NULL)

KEY TECHNIQUE:
- DISTINCT for unique values
- LIMIT with OFFSET for positional selection
- Scalar subquery for NULL handling
- ORDER BY DESC for descending sort

EDGE CASES:
- Single employee: OFFSET 1 returns nothing, result is NULL ✓
- All same salary: DISTINCT returns one value, OFFSET 1 returns NULL ✓
- Two distinct salaries: Returns the lower one ✓
- Duplicate second highest: DISTINCT treats as single value ✓
- Empty table: Subquery returns NULL ✓

CONCEPTS USED:
- Scalar subquery in SELECT clause
- DISTINCT for unique values
- ORDER BY DESC for descending sort
- LIMIT with OFFSET for pagination
- Automatic NULL handling with subquery
- Column aliasing
*/

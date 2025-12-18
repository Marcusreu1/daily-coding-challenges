-- 1789. Primary Department for Each Employee
-- Difficulty: Easy
-- https://leetcode.com/problems/primary-department-for-each-employee/

/*
PROBLEM:
Find the primary department for each employee.
- If an employee belongs to multiple departments, select the one with primary_flag = 'Y'
- If an employee belongs to only one department, select that department (regardless of flag)

TABLES:
- Employee (employee_id, department_id, primary_flag)
  - primary_flag: 'Y' if primary department, 'N' otherwise

EXPECTED OUTPUT:
| employee_id | department_id |
|-------------|---------------|
| 1           | 1             |
| 2           | 1             |
| 3           | 3             |
| 4           | 3             |

EXAMPLE:
Input data:
| employee_id | department_id | primary_flag |
|-------------|---------------|--------------|
| 1           | 1             | N            |
| 2           | 1             | Y            |
| 2           | 2             | N            |
| 3           | 3             | N            |
| 4           | 2             | N            |
| 4           | 3             | Y            |
| 4           | 4             | N            |

Analysis:
Employee 1:
  - Departments: 1 (N)
  - Only 1 department → Select department 1 ✓

Employee 2:
  - Departments: 1 (Y), 2 (N)
  - Multiple departments → Select primary (Y) → department 1 ✓

Employee 3:
  - Departments: 3 (N)
  - Only 1 department → Select department 3 ✓

Employee 4:
  - Departments: 2 (N), 3 (Y), 4 (N)
  - Multiple departments → Select primary (Y) → department 3 ✓
*/

-- STEP 1: Identify two cases
-- CASE 1: primary_flag = 'Y' (employee in multiple depts, select primary)
-- CASE 2: Employee has only 1 department (select that one)

-- STEP 2: Main query filters with OR condition
-- WHERE primary_flag = 'Y' → captures CASE 1

-- STEP 3: Subquery identifies employees with single department
-- GROUP BY employee_id + HAVING COUNT(*) = 1
-- Returns employee_ids that appear only once in Employee table

-- STEP 4: OR employee_id IN (...) → captures CASE 2
-- If employee not in multiple depts, select their single dept

SELECT 
    employee_id,                                             -- Employee ID
    department_id                                            -- Their primary department
FROM Employee
WHERE primary_flag = 'Y'                                     -- CASE 1: Dept marked as primary
   OR employee_id IN (                                       -- CASE 2: Employee with single dept
       SELECT employee_id 
       FROM Employee 
       GROUP BY employee_id 
       HAVING COUNT(*) = 1                                   -- Only 1 department total
   );

/*
WHY EACH PART:
- WHERE primary_flag = 'Y':
  Selects departments marked as primary
  - Employee 2: department 1 has flag 'Y' → selected ✓
  - Employee 4: department 3 has flag 'Y' → selected ✓
  - Handles employees in multiple departments
  
- OR: Logical operator combining two conditions
  If EITHER condition is true, row is included
  - Allows capturing both CASE 1 and CASE 2 in single query
  
- employee_id IN (subquery):
  Checks if employee belongs to set returned by subquery
  - Subquery returns: {1, 3} (employees with only 1 dept)
  - Employee 1 IN {1, 3} → TRUE → included ✓
  - Employee 2 IN {1, 3} → FALSE → not included via this condition
  
- Subquery: SELECT employee_id ... HAVING COUNT(*) = 1
  Finds employees who appear exactly once in Employee table
  - Employee 1: 1 row → COUNT = 1 ✓
  - Employee 2: 2 rows → COUNT = 2 ✗
  - Employee 3: 1 row → COUNT = 1 ✓
  - Employee 4: 3 rows → COUNT = 3 ✗
  - Returns: employee_ids {1, 3}
  
- GROUP BY employee_id:
  Groups all department rows per employee
  - Necessary for COUNT(*) to count departments per employee
  
- HAVING COUNT(*) = 1:
  Filters groups to employees with exactly 1 department
  - HAVING (not WHERE) because filtering aggregated result

KEY CONCEPT - OR Logic for Multiple Cases:
Instead of UNION, use OR to combine conditions:
- Condition A: primary_flag = 'Y' (explicit primary)
- Condition B: employee has only 1 dept (implicit primary)
- Result: A OR B → returns rows matching either condition

Truth table:
| Employee | Flag='Y' | Single Dept | A OR B | Result   |
|----------|----------|-------------|--------|----------|
| 1        | FALSE    | TRUE        | TRUE   | Include  |
| 2 dept1  | TRUE     | FALSE       | TRUE   | Include  |
| 2 dept2  | FALSE    | FALSE       | FALSE  | Exclude  |
| 3        | FALSE    | TRUE        | TRUE   | Include  |
| 4 dept3  | TRUE     | FALSE       | TRUE   | Include  |
| 4 dept2  | FALSE    | FALSE       | FALSE  | Exclude  |

WHY THIS WORKS:
- Employee with primary_flag='Y': Matched by first condition ✓
- Employee with 1 dept and flag='N': Matched by second condition ✓
- Employee with multiple depts and flag='N': Not matched ✓ (correct exclusion)

ALTERNATIVE APPROACHES:
1. Using UNION:
   SELECT employee_id, department_id
   FROM Employee
   WHERE primary_flag = 'Y'
   UNION
   SELECT employee_id, department_id
   FROM Employee
   GROUP BY employee_id
   HAVING COUNT(*) = 1;
   (More explicit, but duplicates code)

2. Using NOT IN (inverse logic):
   SELECT employee_id, department_id
   FROM Employee
   WHERE primary_flag = 'Y'
      OR employee_id NOT IN (
          SELECT employee_id 
          FROM Employee 
          WHERE primary_flag = 'Y'
      );
   (Logic: If employee doesn't have primary flag, must have only 1 dept)

COMPARISON OF APPROACHES:
| Approach    | Readability | Performance | Lines |
|-------------|-------------|-------------|-------|
| OR + IN     | High        | Good        | 7     | ✓ Best balance
| UNION       | High        | Good        | 10    |
| NOT IN      | Medium      | Good        | 7     |
| Window Fn   | Low         | Better      | 12    |

EDGE CASES:
- Employee with 1 dept, flag='Y': Matched by BOTH conditions (no duplicate due to OR) ✓
- Employee with 1 dept, flag='N': Matched by second condition ✓
- Employee with 3 depts, 1 flag='Y': Matched by first condition (only Y dept) ✓
- Employee with 2 depts, both flag='N': NOT matched ✗ (correct, violates constraint)
- All employees have flag='Y': First condition handles all ✓
- No employees have flag='Y': Second condition handles all ✓

EXECUTION ORDER:
1. Subquery executes: finds employees with COUNT(*) = 1
2. Main query evaluates WHERE clause for each row
3. For each row: checks if flag='Y' OR employee in subquery result
4. Returns all matching rows

PERFORMANCE NOTES:
- Subquery executes once (not per row if optimizer is good)
- IN operator efficiently checks membership
- Could add index on (employee_id, primary_flag) for optimization
- UNION approach scans table twice; OR approach scans once

CONCEPTS USED:
- OR operator for multiple conditions
- Subquery in WHERE clause with IN
- GROUP BY for aggregation
- HAVING for filtering aggregated results
- COUNT(*) to count rows per group
- Conditional logic without CASE WHEN
- Handling multiple business rules in single query
*/

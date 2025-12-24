-- 1978. Employees Whose Manager Left the Company
-- Difficulty: Easy
-- https://leetcode.com/problems/employees-whose-manager-left-the-company/

/*
PROBLEM:
Find the IDs of employees whose salary is less than $30,000 AND whose manager 
is no longer with the company (manager_id does not exist as employee_id in the table).

Exclude employees without a manager (manager_id IS NULL).

Order results by employee_id.

TABLES:
- Employees (employee_id PK, name, manager_id, salary)

EXPECTED OUTPUT:
| employee_id |
|-------------|
| 11          |

EXAMPLE:
Employee 11 (Joziah):
  - Salary: $28,485 < $30,000 ✓
  - manager_id: 6 (NOT in table) ✓
  - Result: INCLUDED

Employee 1 (Kalel):
  - Salary: $21,241 < $30,000 ✓
  - manager_id: 11 (EXISTS in table) ✗
  - Result: EXCLUDED

Employee 13 (Emery):
  - Salary: $67,084 > $30,000 ✗
  - Result: EXCLUDED
*/

-- STEP 1: Filter by salary threshold
-- WHERE salary < 30000 keeps only low-paid employees

-- STEP 2: Exclude employees without manager
-- manager_id IS NOT NULL removes top-level employees (CEO, etc.)

-- STEP 3: Check if manager left the company
-- NOT IN (subquery) verifies manager_id doesn't exist as employee_id
-- Subquery returns all current employee_id values

-- STEP 4: Order results
-- ORDER BY employee_id for consistent output

SELECT 
    employee_id
FROM Employees
WHERE salary < 30000                                                             -- Filter: low salary
    AND manager_id IS NOT NULL                                                   -- Exclude: no manager (CEO)
    AND manager_id NOT IN (                                                      -- Filter: manager left
        SELECT employee_id                                                       -- All current employees
        FROM Employees
    )
ORDER BY employee_id;                                                            -- Sort by ID

/*
WHY EACH PART:
- salary < 30000: First condition (low salary threshold)
- manager_id IS NOT NULL: Excludes employees without a manager (top-level)
- NOT IN (subquery): Verifies manager_id is NOT in the list of current employees
- Subquery: Returns all employee_id values (current employees in the company)
- ORDER BY: Ensures consistent, sorted output

WHY manager_id IS NOT NULL:
- Without this check, employees with NULL manager_id would be included
- NULL NOT IN (...) evaluates differently and could produce unexpected results
- The problem explicitly asks for employees "whose manager left" (implies they had one)

KEY TECHNIQUE:
- NOT IN with subquery: Check if value does NOT exist in another set
- Multiple WHERE conditions: Combine filters with AND
- Subquery returns single column: Used for membership testing

ALTERNATIVE APPROACH (LEFT JOIN):
SELECT e1.employee_id
FROM Employees e1
LEFT JOIN Employees e2 ON e1.manager_id = e2.employee_id
WHERE e1.salary < 30000
    AND e1.manager_id IS NOT NULL
    AND e2.employee_id IS NULL                                                   -- Manager not found
ORDER BY e1.employee_id;

-- LEFT JOIN + IS NULL checks for non-existence (equivalent to NOT IN)
-- May perform better on large datasets (depends on indexes)

EDGE CASES:
- Employee with NULL manager_id: Excluded by IS NOT NULL check
- Manager exists in table: Excluded by NOT IN condition
- Multiple employees with same missing manager: All included if salary < 30000
- Empty subquery result: Would include all employees (but shouldn't happen)

CONCEPTS USED:
- Subquery in WHERE clause
- NOT IN operator
- IS NOT NULL
- Multiple AND conditions
- ORDER BY
*/

-- 1731. The Number of Employees Which Report to Each Employee
-- Difficulty: Easy
-- https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/

/*
PROBLEM:
For each manager (employee who has at least one direct report), find:
- employee_id and name of the manager
- Number of employees reporting to them (reports_count)
- Average age of employees reporting to them, rounded to nearest integer (average_age)
Return result ordered by employee_id.

TABLES:
- Employees (employee_id, name, reports_to, age)
  - reports_to: employee_id of the manager (NULL if no manager)

EXPECTED OUTPUT:
| employee_id | name  | reports_count | average_age |
|-------------|-------|---------------|-------------|
| 9           | Hercy | 2             | 39          |

EXAMPLE:
Input data:
| employee_id | name    | reports_to | age |
|-------------|---------|------------|-----|
| 9           | Hercy   | NULL       | 43  |
| 6           | Alice   | 9          | 41  |
| 4           | Bob     | 9          | 36  |
| 2           | Winston | NULL       | 37  |

Analysis:
Employee 9 (Hercy):
  - Direct reports: Alice (41 years), Bob (36 years)
  - reports_count: 2
  - average_age: (41 + 36) / 2 = 38.5 → ROUND = 39

Employee 2 (Winston):
  - Direct reports: None
  - NOT included in result (no reports)

Result: Only Hercy appears (has at least 1 report)
*/

-- STEP 1: Self JOIN to connect managers with their direct reports
-- e (left table): managers
-- a (right table): employees who report to managers
-- JOIN condition: e.employee_id = a.reports_to links manager to their reports

-- STEP 2: Filter to only managers who have reports
-- WHERE a.reports_to IS NOT NULL excludes employees with no direct reports

-- STEP 3: Aggregate per manager
-- GROUP BY e.employee_id, e.name groups all reports per manager
-- COUNT(a.reports_to) counts number of direct reports
-- AVG(a.age) calculates average age of reports
-- ROUND(..., 0) rounds to nearest integer

-- STEP 4: Order by employee_id
-- ORDER BY e.employee_id sorts managers in ascending order

SELECT 
    e.employee_id,                                           -- Manager's employee_id
    e.name,                                                  -- Manager's name
    COUNT(a.reports_to) AS reports_count,                    -- Number of direct reports
    ROUND(AVG(a.age * 1), 0) AS average_age                  -- Average age of reports (rounded)
FROM Employees e
LEFT JOIN Employees a                                        -- Self join: connect employees
    ON e.employee_id = a.reports_to                          -- e is manager, a are reports
WHERE a.reports_to IS NOT NULL                               -- Filter: only managers with reports
GROUP BY e.employee_id, e.name                               -- Aggregate per manager
ORDER BY e.employee_id;                                      -- Sort by manager ID

/*
WHY EACH PART:
- Self JOIN (Employees e JOIN Employees a):
  Creates pairs of (manager, employee) relationships
  - e represents potential managers (left side)
  - a represents employees who report (right side)
  - Same table used twice with different aliases
  
- ON e.employee_id = a.reports_to:
  Join condition that links manager to their direct reports
  - e.employee_id = 9 (Hercy)
  - a.reports_to = 9 (Alice and Bob report to 9)
  - Creates rows: (9, Hercy, Alice), (9, Hercy, Bob)
  
- LEFT JOIN (vs INNER JOIN):
  Includes managers even if they have no reports
  - However, WHERE a.reports_to IS NOT NULL filters them out anyway
  - Could use INNER JOIN for same result
  - LEFT JOIN is more defensive 
  
- WHERE a.reports_to IS NOT NULL:
  Filters to only managers who have at least one direct report
  - Employee 9: has reports (Alice, Bob) → included ✓
  - Employee 2: no reports → a.reports_to is NULL → excluded ✗
  - Without this: Would include employees with 0 reports
  
- COUNT(a.reports_to): Counts number of direct reports
  - Employee 9: COUNT = 2 (Alice and Bob)
  - Counts non-NULL values in a.reports_to column
  - Alternative: COUNT(*) or COUNT(a.employee_id) (same result after WHERE filter)
  
- AVG(a.age * 1): Calculates average age of direct reports
  - Employee 9's reports: ages 41, 36
  - AVG = (41 + 36) / 2 = 38.5
  - Multiplication by 1 ensures numeric type (not always necessary)
  
- ROUND(..., 0): Rounds to nearest integer
  - 38.5 → 39
  - Second parameter 0 means 0 decimal places
  - ROUND(38.5, 0) = 39 (rounds up)
  - ROUND(38.4, 0) = 38 (rounds down)
  
- GROUP BY e.employee_id, e.name:
  Aggregates all reports per manager
  - Groups all rows with same manager into one result row
  - Both columns needed because both are in SELECT (non-aggregated)
  - Could also write: GROUP BY e.employee_id (if name is functionally dependent)
  
- ORDER BY e.employee_id:
  Sorts managers in ascending order by their employee_id
  - Ensures consistent output order
  - Required by problem specification

KEY CONCEPT - SELF JOIN for Hierarchical Relationships:
Self JOIN connects rows within same table based on relationships.

Pattern for manager-employee hierarchy:
- Manager side: e.employee_id (the manager)
- Employee side: a.reports_to (references the manager)
- Join: e.employee_id = a.reports_to

Visualization:
Manager Table (e)          Employee Table (a)
employee_id = 9     ←──────  reports_to = 9 (Alice)
                    ←──────  reports_to = 9 (Bob)

Result: Manager 9 has 2 reports

ALTERNATIVE APPROACHES:
1. Using INNER JOIN instead of LEFT JOIN:
   FROM Employees e
   INNER JOIN Employees a ON e.employee_id = a.reports_to
   (Same result since WHERE filters NULLs anyway)

2. Using subquery for aggregation:
   SELECT 
       e.employee_id,
       e.name,
       (SELECT COUNT(*) FROM Employees WHERE reports_to = e.employee_id) AS reports_count,
       (SELECT ROUND(AVG(age), 0) FROM Employees WHERE reports_to = e.employee_id) AS average_age
   FROM Employees e
   WHERE e.employee_id IN (SELECT DISTINCT reports_to FROM Employees WHERE reports_to IS NOT NULL)
   ORDER BY e.employee_id;

3. Using HAVING instead of WHERE:
   FROM Employees e
   LEFT JOIN Employees a ON e.employee_id = a.reports_to
   GROUP BY e.employee_id, e.name
   HAVING COUNT(a.reports_to) > 0
   (Filters after aggregation instead of before)

WHY AVG(a.age * 1)?
The * 1 multiplication:
- Ensures age is treated as numeric type
- Not strictly necessary in most SQL dialects (age is already numeric)
- Defensive programming to avoid type issues
- Could also write: AVG(a.age) or AVG(CAST(a.age AS DECIMAL))

EDGE CASES:
- Manager with 1 report: reports_count = 1, average_age = that person's age ✓
- Manager with multiple reports: Correctly aggregates ✓
- Employee with no reports: Excluded by WHERE clause ✓
- Employee who is not a manager: reports_to is their manager, not included in result ✓
- NULL ages: AVG ignores NULL values (standard SQL behavior) ✓
- Fractional average age: ROUND handles correctly (38.5 → 39) ✓

EXECUTION ORDER:
1. Self JOIN creates manager-report pairs
2. WHERE filters to only rows where employee has a manager (reports exist)
3. GROUP BY aggregates per manager
4. COUNT and AVG calculate aggregates per group
5. ROUND applies to average
6. ORDER BY sorts final result

CONCEPTS USED:
- Self JOIN for hierarchical relationships
- LEFT JOIN (could be INNER JOIN)
- WHERE clause for filtering
- GROUP BY for aggregation per manager
- COUNT() to count direct reports
- AVG() to calculate average age
- ROUND() to round to integer
- ORDER BY for sorting
- Manager-employee hierarchy pattern
*/

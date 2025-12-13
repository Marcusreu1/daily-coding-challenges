-- 596. Classes With at Least 5 Students
-- Difficulty: Easy
-- https://leetcode.com/problems/classes-more-than-5-students/

/*
PROBLEM:
Find all classes that have at least 5 students enrolled.

TABLES:
- Courses (student, class)

EXPECTED OUTPUT:
| class    |
|----------|
| Math     |
| English  |

EXAMPLE:
Input data:
| student | class    |
|---------|----------|
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |

Math class:
  - Students: A, C, E, G, H, I = 6 students ✓ (>= 5)
  
English class:
  - Students: B = 1 student ✗ (< 5)
  
Biology class:
  - Students: D = 1 student ✗ (< 5)
  
Computer class:
  - Students: F = 1 student ✗ (< 5)

Result: Only Math has at least 5 students
*/

-- STEP 1: GROUP BY class
-- Groups all rows by class name, preparing for aggregation

-- STEP 2: COUNT students per class
-- COUNT(student) counts total enrollments per class

-- STEP 3: Filter with HAVING COUNT(student) >= 5
-- HAVING filters AFTER aggregation (unlike WHERE which filters BEFORE)
-- Only returns classes with 5 or more students

SELECT 
    class                                                    -- Class name
FROM Courses
GROUP BY class                                               -- Group rows by class
HAVING COUNT(student) >= 5;                                  -- Filter groups with at least 5 students

/*
WHY EACH PART:
- GROUP BY class: Collapses all rows with same class into one group
  - Math: A, C, E, G, H, I → becomes 1 group
  - English: B → becomes 1 group
  
- COUNT(student): Counts number of students in each group
  - Math group: COUNT = 6
  - English group: COUNT = 1
  
- HAVING (not WHERE): Filters AFTER grouping
  - WHERE filters individual rows BEFORE grouping
  - HAVING filters groups AFTER aggregation
  - Example: WHERE COUNT(student) >= 5 would ERROR (can't use aggregates in WHERE)
  
- >= 5: Condition for "at least 5 students"
  - Includes exactly 5: COUNT = 5 ✓
  - Includes more than 5: COUNT = 6 ✓
  - Excludes less than 5: COUNT = 4 ✗

KEY CONCEPT - WHERE vs HAVING:
WHERE:  Filters rows BEFORE aggregation (individual records)
HAVING: Filters groups AFTER aggregation (aggregated results)

Example:
WHERE student != 'A'        ✓ Valid: filters individual students
WHERE COUNT(student) >= 5   ✗ Invalid: can't use aggregate in WHERE
HAVING COUNT(student) >= 5  ✓ Valid: filters grouped results

ALTERNATIVE APPROACHES:
1. Using COUNT(*) instead of COUNT(student):
   HAVING COUNT(*) >= 5
   (Same result, counts all rows in group)

CONCEPTS USED:
- GROUP BY for aggregating by category
- COUNT() aggregate function
- HAVING clause for filtering aggregated results
- Difference between WHERE (pre-aggregation) and HAVING (post-aggregation)
*/

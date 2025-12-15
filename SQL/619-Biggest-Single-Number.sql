-- 619. Biggest Single Number
-- Difficulty: Easy
-- https://leetcode.com/problems/biggest-single-number/

/*
PROBLEM:
Find the largest number that appears only once in the table.
If there is no single number, return null.
A "single number" is a number that appears exactly once.

TABLES:
- MyNumbers (num)

EXPECTED OUTPUT:
| num  |
|------|
| 6    |

EXAMPLE 1:
Input data:
| num |
|-----|
| 8   |
| 8   |
| 3   |
| 3   |
| 1   |
| 4   |
| 5   |
| 6   |

Numbers that appear once (single numbers):
  - 1: appears 1 time ✓
  - 4: appears 1 time ✓
  - 5: appears 1 time ✓
  - 6: appears 1 time ✓

Numbers that appear more than once (NOT single):
  - 8: appears 2 times ✗
  - 3: appears 2 times ✗

Largest single number: max(1, 4, 5, 6) = 6

EXAMPLE 2:
Input data:
| num |
|-----|
| 8   |
| 8   |
| 7   |
| 7   |

All numbers appear twice, no single numbers exist.
Result: null
*/

-- STEP 1: Inner query finds all single numbers
-- GROUP BY num groups identical numbers together
-- HAVING COUNT(num) = 1 filters to numbers appearing exactly once

-- STEP 2: ORDER BY num DESC sorts single numbers from largest to smallest
-- This puts the biggest single number first

-- STEP 3: LIMIT 1 takes only the first row (the largest single number)
-- If no single numbers exist, subquery returns NULL

-- STEP 4: Outer SELECT wraps result
-- Ensures NULL is returned when no single number exists
-- Without outer SELECT, empty result set would not show NULL row

SELECT (
    SELECT num                                               -- Select the number
    FROM MyNumbers
    GROUP BY num                                             -- Group identical numbers
    HAVING COUNT(num) = 1                                    -- Filter to single occurrences
    ORDER BY num DESC                                        -- Sort descending (largest first)
    LIMIT 1                                                  -- Take only the biggest one
) AS num;                                                    -- Alias as 'num'

/*
WHY EACH PART:
- GROUP BY num: Creates groups of identical numbers
  - Group {8, 8}: COUNT = 2
  - Group {3, 3}: COUNT = 2
  - Group {1}: COUNT = 1
  - Group {4}: COUNT = 1
  - Group {5}: COUNT = 1
  - Group {6}: COUNT = 1

- HAVING COUNT(num) = 1: Filters to single numbers only
  - Keeps: 1, 4, 5, 6
  - Removes: 8, 3
  - Note: COUNT(num) counts non-NULL values in each group
  
- ORDER BY num DESC: Sorts from highest to lowest
  - Single numbers: 6, 5, 4, 1
  - DESC = descending order (largest first)
  
- LIMIT 1: Takes only first row after sorting
  - Gets: 6 (the biggest single number)
  - Without LIMIT 1 would return all single numbers
  
- Outer SELECT (...) AS num: Handles NULL case
  - If inner query returns no rows → result is NULL
  - Ensures output always has exactly 1 row
  - Example: When all numbers appear multiple times

KEY CONCEPT - Subquery in SELECT:
SELECT (subquery) AS alias
- Subquery must return single value (scalar subquery)
- If subquery returns 0 rows → NULL
- If subquery returns multiple rows → ERROR
- LIMIT 1 ensures single row return

WHY OUTER SELECT IS NEEDED:
Without outer SELECT:
- No single numbers → empty result set (0 rows)
- Problem requires: return NULL (1 row with NULL value)

With outer SELECT:
- No single numbers → subquery returns NULL → output is 1 row with NULL ✓

EXECUTION ORDER:
1. Inner query groups and filters single numbers
2. Inner query sorts descending
3. Inner query limits to 1 result
4. Outer query wraps result (handles NULL case)

EDGE CASES:
- All numbers appear once: Returns largest ✓
- No numbers appear once: Returns NULL ✓
- Empty table: Returns NULL ✓
- Only one number total: If appears once → returns it, if appears multiple times → NULL ✓

CONCEPTS USED:
- GROUP BY for counting occurrences
- HAVING with COUNT() to filter aggregated results
- ORDER BY DESC for descending sort
- LIMIT 1 to get top result
- Scalar subquery in SELECT clause
- NULL handling for empty result sets
*/

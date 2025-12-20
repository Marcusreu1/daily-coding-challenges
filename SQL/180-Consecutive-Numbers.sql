-- 180. Consecutive Numbers
-- Difficulty: Medium
-- https://leetcode.com/problems/consecutive-numbers/

/*
PROBLEM:
Find all numbers that appear at least three times consecutively in the Logs table.
Return the result table with distinct numbers that meet this criteria.

TABLES:
- Logs (id, num)
  - id: unique identifier (auto-increment)
  - num: the number value

EXPECTED OUTPUT:
| ConsecutiveNums |
|-----------------|
| 1               |

EXAMPLE:
Input data:
| id | num |
|----|-----|
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |

Analysis:
Number 1 appears consecutively:
  - id=1: num=1
  - id=2: num=1
  - id=3: num=1
  → Three consecutive rows with same value ✓

Number 2 does NOT appear 3 times consecutively:
  - id=4: num=2 (only once)
  - id=6: num=2
  - id=7: num=2
  → ids 6,7 are consecutive but only 2 times (not 3) ✗

Number 1 at id=5:
  - Appears alone, not part of 3 consecutive ✗

Result: Only number 1 qualifies (appears at ids 1,2,3)
*/

-- STEP 1: Self JOIN the table three times
-- l1 represents the first row in potential sequence
-- l2 represents the second row (id must be l1.id + 1)
-- l3 represents the third row (id must be l2.id + 1)

-- STEP 2: JOIN conditions ensure consecutive ids
-- l1.id + 1 = l2.id means l2 immediately follows l1
-- l2.id + 1 = l3.id means l3 immediately follows l2
-- This creates triplets of consecutive rows

-- STEP 3: WHERE filters for same value across all 3 rows
-- l1.num = l2.num ensures first two rows have same number
-- l2.num = l3.num ensures second and third rows have same number
-- Combined: all three rows have identical num value

-- STEP 4: DISTINCT eliminates duplicate results
-- Same number could appear in multiple consecutive triplets

SELECT DISTINCT 
    l1.num AS ConsecutiveNums                                -- The number appearing 3+ times consecutively
FROM Logs l1
JOIN Logs l2 ON l1.id + 1 = l2.id                           -- l2 is next row after l1
JOIN Logs l3 ON l2.id + 1 = l3.id                           -- l3 is next row after l2
WHERE l1.num = l2.num                                        -- First and second rows have same num
  AND l2.num = l3.num;                                       -- Second and third rows have same num

/*
WHY EACH PART:
- Triple Self JOIN:
  Connects three rows from same table to form consecutive sequences
  - l1: represents position N
  - l2: represents position N+1
  - l3: represents position N+2
  - Creates all possible triplets of consecutive rows
  
- ON l1.id + 1 = l2.id:
  Ensures l2's id is exactly 1 greater than l1's id
  - Example: l1.id=1 joins with l2.id=2 ✓
  - Example: l1.id=1 does NOT join with l2.id=3 ✗ (not consecutive)
  - Arithmetic: l1.id + 1 calculates next expected id
  
- ON l2.id + 1 = l3.id:
  Ensures l3's id is exactly 1 greater than l2's id
  - Creates chain: l1 → l2 → l3 with consecutive ids
  - Example: if l1.id=1 and l2.id=2, then l3.id must be 3
  
- WHERE l1.num = l2.num:
  Filters to triplets where first two rows have same number
  - Example: (1,1,1) passes first check ✓
  - Example: (1,2,2) fails first check ✗
  
- AND l2.num = l3.num:
  Filters to triplets where last two rows have same number
  - Combined with previous: all three must be equal
  - Example: (1,1,1) passes both checks ✓
  - Example: (1,1,2) fails second check ✗
  
- DISTINCT:
  Removes duplicate numbers from result
  - Number 1 might appear in multiple consecutive triplets:
    * Triplet 1: ids (1,2,3) all have num=1
    * Triplet 2: ids (2,3,4) all have num=1 (overlapping)
  - Without DISTINCT: would return 1 twice
  - With DISTINCT: returns 1 once ✓

KEY CONCEPT - Triple Self JOIN for Consecutive Patterns:
Self JOIN technique to identify sequences in ordered data.

Pattern structure:
- Table aliased 3 times (l1, l2, l3)
- JOIN conditions: consecutive ids (N, N+1, N+2)
- WHERE conditions: matching values across rows

Visual representation:
Original table:        After JOIN:
id | num               l1 | l2 | l3 | Result
---|---                ---|----|----|--------
1  | 1         →       1  | 2  | 3  | Match ✓
2  | 1                 2  | 3  | 4  | No match ✗
3  | 1                 3  | 4  | 5  | No match ✗
4  | 2
5  | 1

How triplets are formed:
l1.id=1 → l2.id=2 → l3.id=3
(1,1,1) all same → included

l1.id=2 → l2.id=3 → l3.id=4
(1,1,2) not all same → excluded

WHY THIS APPROACH WORKS:
- Consecutive ids: Ensures rows are adjacent in sequence
- Same num: Ensures all three rows contain identical value
- Self JOIN: Allows comparing row against other rows in same table
- Triple JOIN: Extends pattern to 3 consecutive rows

ALTERNATIVE APPROACHES:
1. Using LEAD window function:
   SELECT DISTINCT num AS ConsecutiveNums
   FROM (
       SELECT 
           num,
           LEAD(num, 1) OVER (ORDER BY id) AS next_num,
           LEAD(num, 2) OVER (ORDER BY id) AS next_next_num
       FROM Logs
   ) AS windowed
   WHERE num = next_num AND num = next_next_num;

2. Using LAG window function:
   SELECT DISTINCT num AS ConsecutiveNums
   FROM (
       SELECT 
           num,
           LAG(num, 1) OVER (ORDER BY id) AS prev_num,
           LAG(num, 2) OVER (ORDER BY id) AS prev_prev_num
       FROM Logs
   ) AS windowed
   WHERE num = prev_num AND num = prev_prev_num;


COMPARISON OF APPROACHES:
| Approach      | Readability | Performance | SQL Standard | Complexity |
|---------------|-------------|-------------|--------------|------------|
| Triple JOIN   | High        | Good        | Standard     | Low        |
| LEAD/LAG      | High        | Better      | SQL:2003     | Low        |

EDGE CASES:
- Number appears exactly 3 times consecutively: Included ✓
  (1,2,3) all have num=1 → result: 1

- Number appears 4+ times consecutively: Included once (DISTINCT) ✓
  (1,2,3,4) all have num=1 → multiple triplets → DISTINCT returns 1 once

- Number appears 2 times consecutively: NOT included ✗
  (1,2) have num=1 but no l3 → no triplet formed

- Number appears 3 times but NOT consecutive: NOT included ✗
  ids (1,3,5) have num=1 but ids not consecutive (1+1≠3)

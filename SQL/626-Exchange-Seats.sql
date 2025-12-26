-- 626. Exchange Seats
-- Difficulty: Medium
-- https://leetcode.com/problems/exchange-seats/

/*
PROBLEM:
Swap the seats of consecutive students:
- Student with odd id swaps with id+1
- Student with even id swaps with id-1
- If the last id is odd (no pair), it remains unchanged

TABLES:
- Seat (id PK, student)
- id is consecutive integers starting from 1

EXPECTED OUTPUT:
+----+---------+
| id | student |
+----+---------+
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |
+----+---------+

EXAMPLE:
Original id=1 (Abbot, odd, not last) → New id=2
Original id=2 (Doris, even) → New id=1
Original id=3 (Emerson, odd, not last) → New id=4
Original id=4 (Green, even) → New id=3
Original id=5 (Jeames, odd, IS last) → New id=5 (no change)

Result: Students swapped positions, ordered by new id
*/

-- STEP 1: Use CASE to calculate new id for each student
-- Three conditions: odd (not last), even, odd (last)

-- STEP 2: Detect odd ids with modulo
-- id % 2 = 1 means odd id (should swap with next)

-- STEP 3: Check if odd id is the last one
-- Compare with COUNT(*) to detect last student (no pair to swap)

-- STEP 4: Calculate swapped id
-- Odd (not last): id+1 (swap with next)
-- Even: id-1 (swap with previous)
-- Odd (last): id (no change)

-- STEP 5: Keep original student name
-- The student value stays the same, only id changes

-- STEP 6: Order by transformed id
-- Sort by new id to show final seating arrangement

SELECT 
    CASE 
        WHEN id % 2 = 1 AND id != (SELECT COUNT(*) FROM Seat) THEN id + 1       -- Odd, not last: swap with next
        WHEN id % 2 = 0 THEN id - 1                                             -- Even: swap with previous
        ELSE id                                                                  -- Odd, last: no change
    END AS id,
    student
FROM Seat
ORDER BY id ASC;                                                                 -- Sort by new id

/*
WHY EACH PART:
- id % 2 = 1: Detects odd ids (1, 3, 5, ...)
- id % 2 = 0: Detects even ids (2, 4, 6, ...)
- id != (SELECT COUNT(*)): Checks if current id is NOT the last one
- id + 1: Moves odd id to next position (1→2, 3→4, ...)
- id - 1: Moves even id to previous position (2→1, 4→3, ...)
- ELSE id: Keeps last odd id unchanged (no pair to swap)
- ORDER BY id: Sorts by transformed id (final seating order)

WHY COUNT(*) FOR LAST CHECK:
- COUNT(*) returns total number of students
- Since ids are consecutive from 1, last id = total count
- Comparison (id != COUNT) identifies if student has a pair to swap
- More reliable than checking id+1 existence

KEY TECHNIQUE:
- CASE WHEN for conditional transformations
- Modulo operator (%) for odd/even detection
- Subquery for maximum value comparison
- Transform column value while preserving other columns

ALTERNATIVE APPROACH (with MAX):
SELECT 
    CASE 
        WHEN id % 2 = 1 AND id != (SELECT MAX(id) FROM Seat) THEN id + 1
        WHEN id % 2 = 0 THEN id - 1
        ELSE id
    END AS id,
    student
FROM Seat
ORDER BY id;

-- MAX(id) instead of COUNT(*) achieves same result
-- Both identify the last student in the table

EDGE CASES:
- Only 1 student (odd, last): Remains at id=1 (ELSE clause)
- Even number of students: All pairs swap normally (no ELSE case triggered)
- Odd number of students: Last student stays in place (ELSE clause)
- Empty table: Returns empty result

CONCEPTS USED:
- CASE WHEN with multiple conditions
- Modulo operator (%) for odd/even detection
- Subquery in WHERE clause (COUNT aggregate)
- Column aliasing
- ORDER BY on transformed column
*/

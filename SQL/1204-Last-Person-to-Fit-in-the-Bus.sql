
-- 1204. Last Person to Fit in the Bus
-- Difficulty: Medium
-- https://leetcode.com/problems/last-person-to-fit-in-the-bus/

/*
PROBLEM:
Find the name of the last person who can board a bus without exceeding the weight limit of 1000 kg.
People board the bus in order of their turn number.
The cumulative weight must not exceed 1000 kg at any point.

TABLES:
- Queue (person_id, person_name, weight, turn)
  - turn: order in which people board (1, 2, 3, ...)
  - weight: weight of each person in kg

EXPECTED OUTPUT:
| person_name |
|-------------|
| John Cena   |

EXAMPLE:
Input data:
| person_id | person_name | weight | turn |
|-----------|-------------|--------|------|
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |

Analysis (sorted by turn):
turn | person_name | weight | cumulative_weight | Can board?
-----|-------------|--------|-------------------|------------
1    | Alice       | 250    | 250               | ✓ (250 <= 1000)
2    | Alex        | 350    | 600               | ✓ (600 <= 1000)
3    | John Cena   | 400    | 1000              | ✓ (1000 <= 1000)
4    | Marie       | 200    | 1200              | ✗ (1200 > 1000)
5    | Bob         | 175    | 1375              | ✗ (1375 > 1000)
6    | Winston     | 500    | 1875              | ✗ (1875 > 1000)

Last person who can board: John Cena (turn 3, cumulative = 1000)
*/

-- STEP 1: Calculate cumulative weight using window function
-- SUM(weight) OVER (ORDER BY turn) computes running total of weights
-- Each row shows total weight of all people up to that turn

-- STEP 2: Filter to people who can board (cumulative <= 1000)
-- WHERE clause keeps only rows where bus is not overweight

-- STEP 3: Find the LAST person who can board
-- ORDER BY turn DESC puts last valid person first
-- LIMIT 1 selects only that person

SELECT person_name                                           -- Name of last person to board
FROM (
    SELECT 
        person_name,                                         -- Person's name
        turn,                                                -- Boarding order
        SUM(weight) OVER (ORDER BY turn) AS cumulative_weight -- Running total of weight
    FROM Queue
) AS weighted                                                -- Subquery with cumulative weights
WHERE cumulative_weight <= 1000                              -- Filter: within weight limit
ORDER BY turn DESC                                           -- Sort: last person first
LIMIT 1;                                                     -- Take only the last valid person

/*
WHY EACH PART:
- Window Function: SUM(weight) OVER (ORDER BY turn)
  Calculates running total (cumulative sum) of weights
  - OVER: Indicates this is a window function (not regular aggregation)
  - ORDER BY turn: Defines order for accumulation (boarding order)
  - For each row: sums weight from first turn up to current turn
  
  Example calculation:
  turn 1: SUM(250) = 250
  turn 2: SUM(250 + 350) = 600
  turn 3: SUM(250 + 350 + 400) = 1000
  turn 4: SUM(250 + 350 + 400 + 200) = 1200
  
- ORDER BY turn in window function:
  Critical for correct cumulative calculation
  - Must process rows in boarding order (turn 1, 2, 3, ...)
  - Without ORDER BY: would sum all weights (incorrect)
  - Ensures each person boards after previous person
  
- Subquery (derived table):
  Necessary because window functions cannot be used directly in WHERE clause
  - Cannot write: WHERE SUM(weight) OVER (...) <= 1000 (SQL syntax error)
  - Must calculate cumulative_weight first, then filter in outer query
  - Subquery creates temporary result set with cumulative_weight column
  
- WHERE cumulative_weight <= 1000:
  Filters to only people who can board without exceeding limit
  - Removes rows where total weight exceeds bus capacity
  - Example: Excludes Marie (1200), Bob (1375), Winston (1875)
  - Keeps: Alice (250), Alex (600), John Cena (1000)
  
- ORDER BY turn DESC:
  Sorts remaining valid people in reverse boarding order
  - DESC: descending order (highest turn first)
  - Puts last person who can board at top of result
  - Example: John Cena (turn 3) appears before Alex (turn 2)
  
- LIMIT 1:
  Takes only first row after sorting
  - Returns single result: the last person who can board
  - Without LIMIT: would return all people who can board
  - With LIMIT: returns only the final person (John Cena)

KEY CONCEPT - Window Functions vs GROUP BY:
Window functions preserve all rows while performing calculations.

Comparison:
GROUP BY approach:
- SUM(weight) GROUP BY something → collapses rows
- Result: fewer rows than input
- Cannot get row-by-row cumulative totals

Window function approach:
- SUM(weight) OVER (ORDER BY turn) → keeps all rows
- Result: same number of rows as input
- Each row has its own cumulative total ✓

Example difference:
Input: 4 rows
GROUP BY: might return 1-2 rows (collapsed)
OVER(): returns 4 rows (each with cumulative value)

HOW WINDOW FUNCTION PROCESSES ROWS:
For each row, window function defines a "frame" (set of rows to aggregate).

Default frame with ORDER BY:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

Meaning:
- UNBOUNDED PRECEDING: from start of partition
- CURRENT ROW: up to and including current row
- Result: cumulative sum from beginning to current position

Visual representation:
Row 1: [250]                    → SUM = 250
Row 2: [250, 350]               → SUM = 600
Row 3: [250, 350, 400]          → SUM = 1000
Row 4: [250, 350, 400, 200]     → SUM = 1200
       └─────── frame ────────┘

EDGE CASES:
- Exact weight limit (cumulative = 1000): Person can board ✓
  WHERE cumulative_weight <= 1000 includes equality
  
- First person exceeds limit (weight > 1000): No result ✓
  All rows filtered out by WHERE clause
  LIMIT 1 on empty set returns empty result
  
- All people fit (total weight < 1000): Returns last person ✓
  All rows pass WHERE filter
  ORDER BY DESC + LIMIT 1 returns person with highest turn
  
- Single person in queue: Returns that person if weight <= 1000 ✓
  Cumulative weight = their weight
  
- People board out of order in data: Window function sorts correctly ✓
  ORDER BY turn in OVER() ensures correct processing order
  Data order in table doesn't matter
  
- Multiple people with same cumulative at limit:
  Example: persons at turns 5,6 both result in cumulative = 1000
  ORDER BY turn DESC selects person with highest turn (turn 6)
  
- Zero or negative weights: Technically allowed, cumulative still calculated ✓
  (Real scenario would validate positive weights)

EXECUTION ORDER:
1. Subquery processes Queue table:
   - ORDER BY turn sorts rows for window function
   - SUM(weight) OVER() calculates cumulative for each row
   - Result: table with person_name, turn, cumulative_weight
   
2. Outer query filters subquery result:
   - WHERE keeps only cumulative_weight <= 1000
   
3. ORDER BY sorts filtered results:
   - DESC puts highest turn first
   
4. LIMIT 1 takes top row:
   - Returns person_name of last valid boarder

PERFORMANCE CONSIDERATIONS:
- Window functions are highly optimized in modern databases
- Single table scan with efficient accumulation
- Index on turn column can help ORDER BY performance
- Much faster than correlated subqueries or self joins
- For very large datasets, still processes in O(n log n) time

OTHER WINDOW FUNCTIONS:
- AVG() OVER(): running average
- COUNT() OVER(): running count
- MIN()/MAX() OVER(): running min/max
- ROW_NUMBER() OVER(): sequential numbering
- RANK() OVER(): ranking with gaps
- LEAD()/LAG() OVER(): access next/previous rows

CONCEPTS USED:
- Window functions (SUM() OVER())
- Running total / cumulative sum
- ORDER BY in window function for accumulation
- Subquery in FROM clause (derived table)
- WHERE clause for filtering aggregated results
- ORDER BY DESC for reverse sorting
- LIMIT for top-N queries
- Point-in-sequence query pattern
*/

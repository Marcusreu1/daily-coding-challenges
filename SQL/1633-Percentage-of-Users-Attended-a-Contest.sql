-- 1633. Percentage of Users Attended a Contest
-- Difficulty: Easy
-- https://leetcode.com/problems/percentage-of-users-attended-a-contest/

/*
PROBLEM:
Calculate the percentage of users registered for each contest.
Round to 2 decimal places.
Order by percentage (descending), then by contest_id (ascending) if tied.

TABLES:
- Users (user_id, user_name)
- Register (contest_id, user_id)

EXPECTED OUTPUT:
| contest_id | percentage |
|------------|------------|
| 208        | 66.67      |
| 209        | 66.67      |
| 215        | 66.67      |

EXAMPLE:
- Total users: 3
- Contest 208: 2 users → (2/3) * 100 = 66.67%
*/

-- STEP 1: RIGHT JOIN to start from Register table
-- Start from Register because I need contests with their registrations
-- RIGHT JOIN ensures all registrations are included (Users is optional here)

-- STEP 2: COUNT(r.user_id) to count registered users per contest
-- This is the NUMERATOR: how many users registered for each contest
-- GROUP BY contest_id makes this count per contest

-- STEP 3: (SELECT COUNT(*) FROM Users) to get total users
-- This is the DENOMINATOR: total users in the platform
-- Subquery runs once and returns total count (3 in example)

-- STEP 4: Formula for percentage
-- COUNT(r.user_id) * 100.0 / (SELECT COUNT(*) FROM Users)
-- Multiply by 100.0 (not 100) to avoid integer division
-- Example: 2 * 100.0 / 3 = 66.666...

-- STEP 5: ROUND(..., 2) to round to 2 decimals
-- Required by the problem: 66.666... → 66.67

-- STEP 6: ORDER BY percentage DESC, contest_id ASC
-- Primary sort: highest percentage first
-- Tie-breaker: lowest contest_id first

SELECT 
    r.contest_id,                                                              -- Contest identifier
    ROUND(                                                                     -- Round to 2 decimals
        (COUNT(r.user_id) * 100.0 / (SELECT COUNT(*) FROM Users)),            -- Percentage formula
        2
    ) AS percentage                                                            -- Alias for result
FROM Users u                                                                   -- Users table (optional for JOIN)
RIGHT JOIN Register r ON u.user_id = r.user_id                                -- Start from Register (all registrations)
GROUP BY r.contest_id                                                          -- Group by contest (one row per contest)
ORDER BY percentage DESC, r.contest_id ASC;                                    -- Sort: % DESC, then ID ASC

/*
WHY EACH PART:
- RIGHT JOIN: Start from Register table (could also use FROM Register LEFT JOIN Users)
- COUNT(r.user_id): Counts users per contest (numerator)
- Subquery: Gets total users (denominator) - runs once for all rows
- * 100.0: Convert to percentage AND avoid integer division (100.0 is DECIMAL)
- ROUND(..., 2): Format required by problem
- GROUP BY contest_id: One result per contest
- ORDER BY: Sort by percentage (highest first), then contest_id (lowest first) for ties

CONCEPTS USED:
- RIGHT JOIN (or could use FROM Register)
- COUNT() aggregate function
- Subquery for total count
- Percentage calculation with decimal division
- ROUND()
- GROUP BY
- ORDER BY with multiple columns
*/

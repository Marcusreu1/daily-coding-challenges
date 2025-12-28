-- 602. Friend Requests II: Who Has the Most Friends
-- Difficulty: Medium
-- https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/

/*
PROBLEM:
Find the person who has the most friends and the number of friends.
Each accepted friend request creates a bidirectional friendship (counts for both users).
Assume there is only one person with the most friends and no duplicate requests.

TABLES:
- RequestAccepted (requester_id, accepter_id, accept_date)
- (requester_id, accepter_id) is the primary key

EXPECTED OUTPUT:
+----+-----+
| id | num |
+----+-----+
| 3  | 3   |
+----+-----+

EXAMPLE:
Friendships from table:
(1, 2): Person 1 ↔ Person 2
(1, 3): Person 1 ↔ Person 3
(2, 3): Person 2 ↔ Person 3
(3, 4): Person 3 ↔ Person 4

Friend count per person:
- Person 1: 2 friends (2, 3)
- Person 2: 2 friends (1, 3)
- Person 3: 3 friends (1, 2, 4) ← MOST FRIENDS
- Person 4: 1 friend (3)

Result: Person 3 with 3 friends
*/

-- STEP 1: Combine both columns (requester_id and accepter_id) into single column
-- UNION ALL includes both sides of each friendship
-- Each friendship appears twice: once from each person's perspective

-- STEP 2: Group by person id and count occurrences
-- COUNT(*) tallies total friendships per person

-- STEP 3: Sort by friend count descending
-- LIMIT 1 returns person with most friends

SELECT 
    id, 
    COUNT(*) AS num                                                              -- Count total friendships
FROM (
    SELECT requester_id AS id                                                    -- Person as requester
    FROM RequestAccepted
    
    UNION ALL                                                                    -- Combine with
    
    SELECT accepter_id AS id                                                     -- Person as accepter
    FROM RequestAccepted
) AS all_friends                                                                 -- All friendship participations
GROUP BY id                                                                      -- One row per person
ORDER BY num DESC                                                                -- Most friends first
LIMIT 1;                                                                         -- Top person only

/*
WHY EACH PART:
- UNION ALL: Combines requester_id and accepter_id into single column (preserves duplicates)
- Two SELECT statements: Captures both sides of each friendship
- Subquery alias (all_friends): Creates derived table with all participations
- GROUP BY id: Aggregates all friendships per person
- COUNT(*): Counts total friendship occurrences for each person
- ORDER BY num DESC: Sorts from most friends to least
- LIMIT 1: Returns only the person with maximum friends

WHY UNION ALL (not UNION):
- UNION ALL: Keeps all rows (including duplicates) for accurate counting
- UNION: Would remove duplicates, losing friendship counts
- Each friendship must be counted once per person (need duplicates)

KEY TECHNIQUE:
- UNION ALL for dual-column aggregation: Combines values from two columns into one
- Subquery as data source: Transforms table structure before aggregation
- Bidirectional relationship handling: Each row represents friendship for both users

ALTERNATIVE APPROACH (without UNION ALL):
SELECT 
    id, 
    SUM(cnt) AS num
FROM (
    SELECT requester_id AS id, COUNT(*) AS cnt
    FROM RequestAccepted
    GROUP BY requester_id
    
    UNION ALL
    
    SELECT accepter_id AS id, COUNT(*) AS cnt
    FROM RequestAccepted
    GROUP BY accepter_id
) AS counts
GROUP BY id
ORDER BY num DESC
LIMIT 1;

-- Pre-aggregates before UNION ALL (may be more efficient on large datasets)
-- Both approaches produce same result

EDGE CASES:
- Person appears only as requester: Counted correctly via first SELECT
- Person appears only as accepter: Counted correctly via second SELECT
- Person appears in both roles: Both counted via UNION ALL
- Tie for most friends: LIMIT 1 returns one arbitrary result (problem guarantees uniqueness)
- Single friendship row: Both persons have 1 friend each

CONCEPTS USED:
- UNION ALL
- Subquery in FROM clause (derived table)
- GROUP BY aggregation
- COUNT(*) aggregate function
- ORDER BY with DESC
- LIMIT
- Column aliasing
*/

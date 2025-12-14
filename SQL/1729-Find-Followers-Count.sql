-- 1729. Find Followers Count
-- Difficulty: Easy
-- https://leetcode.com/problems/find-followers-count/

/*
PROBLEM:
Find the number of followers for each user.
Return the result table ordered by user_id in ascending order.

TABLES:
- Followers (user_id, follower_id)

EXPECTED OUTPUT:
| user_id | followers_count |
|---------|-----------------|
| 0       | 1               |
| 1       | 1               |
| 2       | 2               |

EXAMPLE:
Input data:
| user_id | follower_id |
|---------|-------------|
| 0       | 1           |
| 1       | 0           |
| 2       | 0           |
| 2       | 1           |

User 0:
  - Followers: 1
  - Count: 1 follower
  
User 1:
  - Followers: 0
  - Count: 1 follower
  
User 2:
  - Followers: 0, 1
  - Count: 2 followers

Result: Ordered by user_id (0, 1, 2)
*/

-- STEP 1: GROUP BY user_id
-- Groups all follower records by the user being followed

-- STEP 2: COUNT followers per user
-- COUNT(follower_id) counts how many followers each user has

-- STEP 3: ORDER BY user_id
-- Sorts result in ascending order by user_id (requirement)

SELECT 
    user_id,                                                 -- User being followed
    COUNT(follower_id) AS followers_count                    -- Number of followers
FROM Followers
GROUP BY user_id                                             -- Group by user
ORDER BY user_id;                                            -- Sort by user_id ascending

/*
WHY EACH PART:
- GROUP BY user_id: Collapses all rows with same user_id
  - User 0: (0, 1) → becomes 1 group
  - User 1: (1, 0) → becomes 1 group
  - User 2: (2, 0), (2, 1) → becomes 1 group
  
- COUNT(follower_id): Counts followers in each group
  - User 0 group: COUNT = 1
  - User 1 group: COUNT = 1
  - User 2 group: COUNT = 2
  
- AS followers_count: Alias for output column name
  - Required by problem specification
  
- ORDER BY user_id: Sorts final result
  - Ascending order (default): 0, 1, 2
  - Could explicitly write: ORDER BY user_id ASC

KEY CONCEPT - ORDER BY with GROUP BY:
ORDER BY is applied AFTER aggregation:
1. GROUP BY groups rows → (user_id, count)
2. ORDER BY sorts grouped results → sorted output

ORDER BY can use:
- Selected columns: ORDER BY user_id ✓
- Aggregated values: ORDER BY COUNT(follower_id) ✓
- Column aliases: ORDER BY followers_count ✓

ALTERNATIVE APPROACHES:
1. Using COUNT(*) instead of COUNT(follower_id):
   SELECT user_id, COUNT(*) AS followers_count
   (Same result, counts all rows in group)

2. Explicit ASC ordering:
   ORDER BY user_id ASC
   (More explicit, but ASC is default)

3. Order by count (descending) instead:
   ORDER BY followers_count DESC, user_id
   (Would show most followed users first)

EDGE CASES:
- User with no followers: Won't appear in result (no row in Followers table)
- User with 1 follower: COUNT = 1 ✓
- User with multiple followers: COUNT = number of rows ✓
- Same follower can't follow same user twice: Assumed based on typical schema

CONCEPTS USED:
- GROUP BY for aggregating by user
- COUNT() aggregate function to count followers
- ORDER BY for sorting results
- Column alias with AS
- Aggregation + Sorting pattern (GROUP BY → ORDER BY)
*/

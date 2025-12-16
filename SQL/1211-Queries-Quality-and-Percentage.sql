-- 1211. Queries Quality and Percentage
-- Difficulty: Easy
-- https://leetcode.com/problems/queries-quality-and-percentage/

/*
PROBLEM:
Calculate two metrics for each query_name:
1. quality: average of (rating/position), rounded to 2 decimals
2. poor_query_percentage: percentage of queries with rating < 3, rounded to 2 decimals

TABLES:
- Queries (query_name, result, position, rating)

EXPECTED OUTPUT:
| query_name | quality | poor_query_percentage |
|------------|---------|----------------------|
| Dog        | 2.50    | 33.33                |
| Cat        | 0.66    | 33.33                |

EXAMPLE (Dog):
- Golden: rating=5, position=1 → 5/1 = 5.0  (rating ≥ 3, not poor)
- Poodle: rating=3, position=2 → 3/2 = 1.5  (rating ≥ 3, not poor)
- Freaky: rating=1, position=3 → 1/3 = 0.33 (rating < 3, POOR!)
- Quality: AVG(5.0, 1.5, 0.33) = 2.28
- Poor %: 1 poor out of 3 total = (1/3) * 100 = 33.33%
*/

-- STEP 1: Calculate quality using AVG(rating/position)
-- Divide rating by position for each row, then average all results
-- Multiply by 1.0 to avoid integer division (e.g., 3/2 = 1 without decimal)

-- STEP 2: Calculate poor_query_percentage
-- Count how many queries have rating < 3
-- SUM(rating < 3) works because boolean returns 1 (true) or 0 (false) in MySQL
-- Divide by COUNT(*) to get proportion, multiply by 100.0 for percentage

-- STEP 3: ROUND both metrics to 2 decimals
-- Required by the problem specification

-- STEP 4: GROUP BY query_name
-- Need one row per query_name with aggregated metrics

SELECT 
    query_name,                                                    -- Query identifier
    ROUND((AVG(rating * 1.0 / position)), 2) AS quality,          -- Metric 1: average quality score
    ROUND((SUM(rating < 3) * 100.0 / COUNT(*)), 2)                -- Metric 2: percentage of poor queries
        AS poor_query_percentage
FROM Queries 
GROUP BY query_name;                                               -- One result per query_name

/*
WHY EACH PART:
- rating * 1.0: Convert to decimal to avoid integer division (3/2 would be 1 instead of 1.5)
- AVG(rating * 1.0 / position): Calculates average of all (rating/position) values
- SUM(rating < 3): Boolean comparison returns 1 if true, 0 if false - sums total poor queries
- COUNT(*): Total number of queries for this query_name
- * 100.0: Convert proportion to percentage (0.33 → 33.33)
- ROUND(..., 2): Format both metrics to 2 decimal places
- GROUP BY: Aggregate all rows with same query_name into single result

CONCEPTS USED:
- AVG() aggregate function
- Division with decimal conversion
- SUM() with boolean expression (MySQL feature)
- COUNT() aggregate function
- Percentage calculation
- ROUND()
- GROUP BY
*/

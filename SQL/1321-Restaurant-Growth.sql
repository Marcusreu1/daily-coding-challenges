-- 1321. Restaurant Growth
-- Difficulty: Medium
-- https://leetcode.com/problems/restaurant-growth/

/*
PROBLEM:
Calculate a 7-day moving window for each day:
- amount: Sum of amounts from the last 7 days (including current day)
- average_amount: Average of amounts from the last 7 days (rounded to 2 decimals)

Only show results starting from the 7th day (when 7 days of data are available).
Order by visited_on.

TABLES:
- Customer (customer_id, name, visited_on, amount)
- (customer_id, visited_on) is the primary key
- Multiple customers can visit on the same day

EXPECTED OUTPUT:
+--------------+--------------+----------------+
| visited_on   | amount       | average_amount |
+--------------+--------------+----------------+
| 2019-01-07   | 860          | 122.86         |
| 2019-01-08   | 840          | 120.00         |
| 2019-01-09   | 840          | 120.00         |
| 2019-01-10   | 1000         | 142.86         |
+--------------+--------------+----------------+

EXAMPLE:
2019-01-07: Sum of days 01-01 to 01-07 = 860, Avg = 860/7 = 122.86
2019-01-08: Sum of days 01-02 to 01-08 = 840, Avg = 840/7 = 120.00
2019-01-10: Sum of days 01-04 to 01-10 = 1000, Avg = 1000/7 = 142.86
(Note: 01-10 has two customers, amounts are summed first)
*/

-- STEP 1: Inner subquery aggregates amounts by day
-- Multiple customers on same day are summed into single daily total
-- GROUP BY visited_on creates one row per unique date

-- STEP 2: Middle subquery applies 7-day moving window
-- RANGE BETWEEN uses date intervals (not row count)
-- Includes current day + 6 previous days = 7 days total
-- MIN(visited_on) OVER() finds earliest date in dataset (for filtering)
-- DISTINCT removes potential duplicates from window function

-- STEP 3: Outer query calculates average and filters results
-- average_amount = amount / 7 (7-day window is always 7 days)
-- Filter: visited_on >= first_date + 6 days (ensures 7 days of data exist)
-- ORDER BY visited_on for chronological output

SELECT 
    visited_on,
    amount,
    ROUND(amount / 7, 2) AS average_amount                                       -- Calculate 7-day average
FROM (
    SELECT DISTINCT
        visited_on,
        SUM(amount) OVER (                                                       -- 7-day moving sum
            ORDER BY visited_on 
            RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW               -- Last 7 days (6 prior + current)
        ) AS amount,
        MIN(visited_on) OVER () AS first_date                                    -- Find earliest date in dataset
    FROM (
        SELECT 
            visited_on, 
            SUM(amount) AS amount                                                -- Sum amounts per day
        FROM Customer
        GROUP BY visited_on                                                      -- One row per unique date
    ) AS daily_totals
) AS windowed
WHERE visited_on >= DATE_ADD(first_date, INTERVAL 6 DAY)                        -- Filter: only days with 7 days of data
ORDER BY visited_on;                                                             -- Chronological order

/*
WHY EACH PART:
- Inner GROUP BY visited_on: Combines multiple customers on same day into single daily total
- SUM(amount) in subquery: Aggregates all transactions for each day
- RANGE BETWEEN INTERVAL 6 DAY: Date-based window (handles missing days correctly)
- 6 DAY PRECEDING + CURRENT ROW: Last 7 calendar days (not 7 rows)
- MIN(visited_on) OVER (): Window function to find first date across all rows
- DISTINCT: Removes duplicates that window function might create
- DATE_ADD(first_date, INTERVAL 6 DAY): First date that has 6 prior days available
- amount / 7: Average calculation (window always spans exactly 7 days)
- ROUND(..., 2): Format to 2 decimal places
- Outer ORDER BY: Final sorting for output

WHY RANGE (not ROWS):
- RANGE BETWEEN INTERVAL 6 DAY: Based on date values (calendar days)
- ROWS BETWEEN 6 PRECEDING: Based on row count (would fail if days are missing)
- Example: If 2019-01-03 has no data, ROWS would include wrong dates
- RANGE correctly includes last 7 calendar days regardless of data gaps

WHY THREE LEVELS OF QUERIES:
1. Inner: Aggregate by day (handle multiple customers per day)
2. Middle: Apply moving window calculation
3. Outer: Calculate average and filter results

WHY MIN(visited_on) OVER():
- Finds the earliest date in entire dataset
- Used to calculate when 7-day window becomes valid (first_date + 6 days)
- OVER () with no partition/order = aggregate over all rows

KEY TECHNIQUE:
- RANGE BETWEEN INTERVAL: Date-based moving window (not row-based)
- Nested aggregation: GROUP BY before window function
- MIN() OVER (): Global aggregate via window function
- DATE_ADD for date arithmetic
- Multi-level subqueries for complex transformations

EDGE CASES:
- Multiple customers on same day: Handled by inner GROUP BY
- Days with no customers: RANGE correctly handles gaps in dates
- Exactly 7 days of data: First result shows on day 7
- Less than 7 days total: Empty result (WHERE filter excludes all)
- First 6 days: Excluded by WHERE clause (insufficient data)

CONCEPTS USED:
- Window functions: SUM() OVER, MIN() OVER
- RANGE BETWEEN INTERVAL (date-based window)
- Nested subqueries (3 levels)
- GROUP BY for daily aggregation
- Date arithmetic with DATE_ADD and INTERVAL
- DISTINCT to handle window function results
- ROUND() for decimal formatting
- Column aliasing
*/

-- 1193. Monthly Transactions I
-- Difficulty: Medium
-- https://leetcode.com/problems/monthly-transactions-i/

/*
PROBLEM:
Calculate transaction statistics grouped by month and country.
For each (month, country) pair, compute:
1. trans_count: total number of transactions
2. approved_count: number of approved transactions
3. trans_total_amount: sum of all transaction amounts
4. approved_total_amount: sum of approved transaction amounts only

TABLES:
- Transactions (id, country, state, amount, trans_date)

EXPECTED OUTPUT:
| month   | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
|---------|---------|-------------|----------------|--------------------|-----------------------|
| 2018-12 | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01 | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01 | DE      | 1           | 1              | 2000               | 2000                  |

EXAMPLE (2018-12, US):
- Trans 121: approved, 1000
- Trans 122: declined, 2000
- trans_count: 2 (all transactions)
- approved_count: 1 (only approved)
- trans_total_amount: 3000 (1000 + 2000)
- approved_total_amount: 1000 (only approved amounts)
*/

-- STEP 1: Extract month from trans_date using DATE_FORMAT
-- Convert full dates (2018-12-18) to year-month format (2018-12)
-- This allows grouping transactions from the same month together

-- STEP 2: Count all transactions per group
-- COUNT(*) counts every row in the group regardless of state

-- STEP 3: Count only approved transactions
-- COUNT(CASE WHEN...) returns 1 for approved, NULL otherwise
-- COUNT ignores NULL values, so it only counts approved transactions

-- STEP 4: Sum all transaction amounts
-- SUM(amount) adds up all amounts regardless of state

-- STEP 5: Sum only approved transaction amounts
-- SUM(CASE WHEN...) adds the amount if approved, 0 otherwise
-- This gives the total money from approved transactions only

-- STEP 6: GROUP BY month and country
-- Creates one result row for each unique (month, country) combination

SELECT 
    DATE_FORMAT(trans_date, '%Y-%m') AS month,                                   -- Extract year-month from date
    country,                                                                      -- Country identifier
    COUNT(*) AS trans_count,                                                     -- Total transactions
    COUNT(CASE WHEN state = 'approved' THEN 1 END) AS approved_count,           -- Count only approved
    SUM(amount) AS trans_total_amount,                                           -- Sum all amounts
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END)                    -- Sum only approved amounts
        AS approved_total_amount
FROM Transactions
GROUP BY DATE_FORMAT(trans_date, '%Y-%m'), country;                              -- Group by month and country

/*
WHY EACH PART:
- DATE_FORMAT(..., '%Y-%m'): Converts dates to 'YYYY-MM' format for monthly grouping
- COUNT(*): Counts all rows in each group (total transactions)
- COUNT(CASE WHEN... THEN 1 END): Returns 1 for approved (counted), NULL otherwise (ignored)
- SUM(amount): Sums all amounts without filtering
- SUM(CASE WHEN... THEN amount ELSE 0 END): Sums amount if approved, 0 if not
- GROUP BY month, country: Creates separate groups for each (month, country) pair

KEY TECHNIQUES:
- Conditional COUNT: COUNT(CASE WHEN condition THEN 1 END) counts only matching rows
- Conditional SUM: SUM(CASE WHEN condition THEN value ELSE 0 END) sums only matching values
- These avoid needing subqueries or multiple passes through the data

CONCEPTS USED:
- DATE_FORMAT() for date manipulation
- COUNT() with CASE for conditional counting
- SUM() with CASE for conditional summing
- GROUP BY with multiple columns
- Aggregate functions with conditional logic
*/

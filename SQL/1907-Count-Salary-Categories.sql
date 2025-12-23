-- 1907. Count Salary Categories
-- Difficulty: Medium
-- https://leetcode.com/problems/count-salary-categories/

/*
PROBLEM:
Count the number of bank accounts in each salary category.
Categories are defined as:
- 'Low Salary': income < 20000
- 'Average Salary': 20000 <= income <= 50000
- 'High Salary': income > 50000

All three categories must appear in the result, even if count is 0.

TABLES:
- Accounts (account_id, income)

EXPECTED OUTPUT:
| category       | accounts_count |
|----------------|----------------|
| Low Salary     | 1              |
| Average Salary | 0              |
| High Salary    | 3              |

EXAMPLE:
Input data:
| account_id | income |
|------------|--------|
| 3          | 108939 |
| 2          | 12747  |
| 8          | 87709  |
| 6          | 91796  |

Analysis by category:
Low Salary (income < 20000):
  - account_id 2: income = 12747 ✓
  - Count: 1

Average Salary (20000 <= income <= 50000):
  - No accounts in this range
  - Count: 0 (must still appear in result)

High Salary (income > 50000):
  - account_id 3, 8, 6 ✓
  - Count: 3
*/

-- STEP 1: Create reference table with ALL categories using UNION
-- Ensures all three categories appear in result even if no accounts match

-- STEP 2: Classify each account into a category using CASE WHEN
-- Subquery a assigns category based on income ranges

-- STEP 3: LEFT JOIN categories with classified accounts
-- LEFT JOIN preserves all categories (c), even those with no matching accounts (a)
-- Unmatched categories will have NULL in a.category

-- STEP 4: Count accounts using SUM with conditional CASE
-- SUM(CASE WHEN a.category IS NOT NULL THEN 1 ELSE 0 END)
-- NULL values contribute 0, non-NULL values contribute 1

SELECT 
    c.category,                                              -- Category name
    SUM(CASE WHEN a.category IS NOT NULL THEN 1 ELSE 0 END) AS accounts_count -- Count of accounts
FROM (
    SELECT 'Low Salary' AS category                          -- Define category 1
    UNION 
    SELECT 'Average Salary'                                  -- Define category 2
    UNION 
    SELECT 'High Salary'                                     -- Define category 3
) c
LEFT JOIN (
    SELECT 
        CASE 
            WHEN income < 20000 THEN 'Low Salary'            -- Income below 20k
            WHEN income BETWEEN 20000 AND 50000 THEN 'Average Salary' -- Income 20k-50k (inclusive)
            ELSE 'High Salary'                               -- Income above 50k
        END AS category
    FROM Accounts
) a ON c.category = a.category                               -- Match accounts to categories
GROUP BY c.category;                                         -- Aggregate counts per category

/*
WHY EACH PART:
- UNION creates reference table:
  Produces 3-row table with all category names
  - Ensures every category appears in final result
  - Without this: categories with 0 accounts would be missing
  
- CASE WHEN for classification:
  Assigns each account to exactly one category based on income
  - Conditions evaluated top to bottom
  - BETWEEN is inclusive: includes 20000 and 50000 in Average Salary
  - ELSE catches all income > 50000
  
- LEFT JOIN (not INNER):
  Preserves ALL categories from left side (c)
  - Categories without matching accounts get NULL in a.category
  - INNER JOIN would exclude categories with no accounts ✗
  - Example: If no Average Salary accounts exist:
    c.category='Average Salary' LEFT JOIN a → a.category=NULL
  
- SUM(CASE WHEN a.category IS NOT NULL THEN 1 ELSE 0):
  Counts non-NULL matches per category
  - When a.category IS NOT NULL: account exists → add 1
  - When a.category IS NULL: no account → add 0
  - Alternative: COUNT(a.account_id) also works (counts non-NULL values)
  
- GROUP BY c.category:
  Aggregates results per salary category
  - Each category becomes one row in final result
  - SUM operates independently on each group

KEY CONCEPT - Bucketing with Zero Counts:
Pattern for counting with guaranteed category presence:
1. Create reference table with ALL categories (UNION)
2. LEFT JOIN data to categories (preserves all categories)
3. Use COUNT(column) or SUM(CASE) to handle NULLs as 0

Visual representation:
Categories (c):          Classified Data (a):
┌───────────────┐        ┌─────────────┐
│ Low Salary    │   ←──  │ Low Salary  │ (1 account)
│ Average Salary│        │ (no match)  │
│ High Salary   │   ←──  │ High Salary │ (3 accounts)
└───────────────┘        └─────────────┘

After LEFT JOIN:
| c.category     | a.category  | Count |
|----------------|-------------|-------|
| Low Salary     | Low Salary  | 1     |
| Average Salary | NULL        | 0     | ← Preserved by LEFT JOIN
| High Salary    | High Salary | 3     |

ALTERNATIVE APPROACHES:
1. Using CTE for readability:
   WITH categories AS (
       SELECT 'Low Salary' AS category
       UNION SELECT 'Average Salary'
       UNION SELECT 'High Salary'
   ),
   classified AS (
       SELECT CASE 
           WHEN income < 20000 THEN 'Low Salary'
           WHEN income BETWEEN 20000 AND 50000 THEN 'Average Salary'
           ELSE 'High Salary'
       END AS category
       FROM Accounts
   )
   SELECT c.category, COUNT(cl.category) AS accounts_count
   FROM categories c
   LEFT JOIN classified cl ON c.category = cl.category
   GROUP BY c.category;

EDGE CASES:
- No accounts in a category: Shows count = 0 ✓
  LEFT JOIN produces NULL, SUM evaluates to 0
  
- All accounts in one category: Other two show 0 ✓
  
- Exact boundary values (20000, 50000): Assigned to Average Salary ✓
  BETWEEN is inclusive on both ends
  
- Empty Accounts table: All categories show count = 0 ✓
  LEFT JOIN finds no matches for any category

CONCEPTS USED:
- UNION to create reference table
- CASE WHEN for categorization
- BETWEEN operator for inclusive ranges
- LEFT JOIN to preserve all categories
- SUM with CASE for conditional counting
- GROUP BY for aggregation
- Pattern: Guaranteed category presence in results
*/

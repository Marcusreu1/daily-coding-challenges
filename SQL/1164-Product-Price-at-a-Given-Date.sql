-- 1164. Product Price at a Given Date
-- Difficulty: Medium
-- https://leetcode.com/problems/product-price-at-a-given-date/

/*
PROBLEM:
Find the price of each product on 2019-08-16.
- If a product had price changes on or before 2019-08-16, use the most recent price
- If a product has NO price changes on or before 2019-08-16, use default price of 10

TABLES:
- Products (product_id, new_price, change_date)
- change_date: date when price was changed to new_price

EXPECTED OUTPUT:
| product_id | price |
|------------|-------|
| 1          | 20    |
| 2          | 50    |
| 3          | 10    |

EXAMPLE:
Input data:
| product_id | new_price | change_date |
|------------|-----------|-------------|
| 1          | 35        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 20        | 2019-08-15  |
| 1          | 30        | 2019-08-17  |
| 3          | 15        | 2019-08-18  |

Analysis for 2019-08-16:

Product 1:
  - 2019-08-14: price = 35
  - 2019-08-15: price = 20 ← Last change on/before 2019-08-16
  - 2019-08-17: price = 30 (after target date, ignored)
  → Price on 2019-08-16: 20

Product 2:
  - 2019-08-14: price = 50 ← Last (and only) change on/before 2019-08-16
  → Price on 2019-08-16: 50

Product 3:
  - 2019-08-18: price = 15 (after target date, ignored)
  - No changes on/before 2019-08-16
  → Price on 2019-08-16: 10 (default)
*/

-- STEP 1: Get all unique product IDs
-- Subquery p: Lists all products that exist in the table
-- Ensures every product appears in final result

-- STEP 2: Find last price on/before 2019-08-16 for each product
-- Subquery p2: Uses pattern (product_id, MAX(change_date)) to find most recent price
-- Filters to change_date <= '2019-08-16' to exclude future changes

-- STEP 3: LEFT JOIN to include all products
-- Products with price changes: matched with p2 (new_price populated)
-- Products without price changes: no match in p2 (new_price is NULL)

-- STEP 4: Use COALESCE to handle NULLs
-- If new_price exists: use it
-- If new_price is NULL: use default price 10

SELECT 
    p.product_id,                                            -- Product identifier
    COALESCE(p2.new_price, 10) AS price                      -- Price on date (or default 10)
FROM (
    SELECT DISTINCT product_id                               -- All unique products
    FROM Products
) p
LEFT JOIN (
    SELECT product_id, new_price                             -- Latest price per product
    FROM Products
    WHERE (product_id, change_date) IN (                     -- Pattern: find last occurrence
        SELECT product_id, MAX(change_date)                  -- Most recent change date
        FROM Products
        WHERE change_date <= '2019-08-16'                    -- On or before target date
        GROUP BY product_id                                  -- Per product
    )
) p2 ON p.product_id = p2.product_id;                        -- Match products

/*
WHY EACH PART:
- Subquery p: SELECT DISTINCT product_id FROM Products
  Gets complete list of all products in system
  - Ensures products with only future changes appear in result
  - Example: Product 3 has no changes before 2019-08-16 but still needs to appear
  - DISTINCT removes duplicates (product may have multiple price changes)
  
- LEFT JOIN (not INNER JOIN):
  Preserves ALL products from left side (p)
  - INNER JOIN: Would exclude products with no price changes before date ✗
  - LEFT JOIN: Includes all products, sets p2.new_price to NULL if no match ✓
  - Product 3 example: appears in p, no match in p2, new_price = NULL
  
- Subquery p2: Price lookup subquery
  Finds products that HAD price changes on/before target date
  - Returns: (product_id, new_price) for matching products only
  - Products without changes: Not in this result set
  
- WHERE (product_id, change_date) IN (...):
  Tuple comparison pattern to find rows with specific combinations
  - Matches rows where BOTH product_id AND change_date match subquery result
  - Used to select the exact row with the latest change date per product
  
- Inner subquery: MAX(change_date) per product
  SELECT product_id, MAX(change_date)
  FROM Products
  WHERE change_date <= '2019-08-16'
  GROUP BY product_id
  
  Result for example data:
  | product_id | MAX(change_date) |
  |------------|------------------|
  | 1          | 2019-08-15       |
  | 2          | 2019-08-14       |
  
  (Product 3 not included: no changes before/on 2019-08-16)
  
- WHERE change_date <= '2019-08-16':
  Filters to only consider price changes on or before target date
  - <= includes the target date itself (if price changed on that exact date)
  - Changes after 2019-08-16 are ignored (future changes don't affect historical price)
  - Example: Product 1's change on 2019-08-17 excluded ✓
  
- GROUP BY product_id:
  Aggregates to find maximum date per product
  - Each product appears once in result
  - MAX(change_date) returns most recent change date for that product
  
- COALESCE(p2.new_price, 10):
  Returns first non-NULL value from arguments
  - If p2.new_price exists: returns p2.new_price (actual price from history)
  - If p2.new_price is NULL: returns 10 (default price)
  - Product 1: new_price = 20 → COALESCE(20, 10) = 20 ✓
  - Product 3: new_price = NULL → COALESCE(NULL, 10) = 10 ✓

KEY CONCEPT - Point-in-Time Query with Default Values:
Finding historical state at specific date with fallback for missing data.

Pattern components:
1. Get all entities (DISTINCT product_id)
2. LEFT JOIN with historical data (changes before date)
3. Use COALESCE for default value (when no history)

Query logic:
- Filters: changes <= 2019-08-16 → {35, 20}
- MAX(date): 2019-08-15
- Price: 20 ✓

Query logic:
- Filters: changes <= 2019-08-16 → {} (empty)
- No match in p2: new_price = NULL
- COALESCE(NULL, 10) = 10 ✓

EDGE CASES:
- Product with price change exactly on 2019-08-16: Included (<=) ✓
  change_date = '2019-08-16' → filtered in → used as latest price
  
- Product with multiple changes before date: Uses most recent ✓
  changes: 2019-08-10, 2019-08-12, 2019-08-14
  → MAX(change_date) = 2019-08-14 → uses that price
  
- Product with only changes after date: Uses default 10 ✓
  change_date = '2019-08-20' → filtered out → NULL → default 10
  
- Product with changes both before and after: Uses last one before ✓
  changes: 2019-08-14 (50), 2019-08-18 (60)
  → Only considers 2019-08-14 → price = 50
  
- Product with same price on multiple dates: Handled correctly ✓
  changes: 2019-08-10 (30), 2019-08-12 (30)
  → MAX(date) = 2019-08-12 → price = 30
  
- Empty Products table: Returns empty result ✓
  No products exist → p subquery returns empty → final result empty
  
- All products have only future changes: All get default 10 ✓
  All change_date > '2019-08-16' → p2 empty → all NULL → all default

EXECUTION ORDER:
1. Innermost subquery: Find MAX(change_date) per product (before target date)
2. Middle subquery (p2): Get product_id and new_price for those max dates
3. Left subquery (p): Get all distinct product_ids
4. LEFT JOIN: Combine all products with their prices (NULL if no match)
5. COALESCE: Replace NULL with default value 10
6. SELECT: Return product_id and price

PERFORMANCE CONSIDERATIONS:
- Index on (product_id, change_date) improves MAX() lookup
- Index on (change_date, product_id) helps WHERE filtering
- DISTINCT in subquery p may scan full table
- Alternative: Use product dimension table if available
- For large datasets, window functions may be more efficient

WHY COALESCE IS BETTER THAN IFNULL/NVL:
- COALESCE: SQL standard, works across all databases
- IFNULL: MySQL/SQLite specific, takes only 2 arguments
- NVL: Oracle specific
- COALESCE can handle multiple arguments: COALESCE(val1, val2, val3, default)

CONCEPTS USED:
- Subquery in FROM clause (derived table)
- LEFT JOIN for preserving all rows from left table
- Tuple comparison with IN: (col1, col2) IN (subquery)
- MAX() aggregate function for finding latest date
- GROUP BY for aggregation per product
- COALESCE() for NULL handling with default value
- DISTINCT for removing duplicates
- WHERE with date comparison (<=)
- Point-in-time query pattern
- Historical data lookup with fallback
*/

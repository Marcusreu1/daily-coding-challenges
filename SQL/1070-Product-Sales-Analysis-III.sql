-- 1070. Product Sales Analysis III
-- Difficulty: Medium
-- https://leetcode.com/problems/product-sales-analysis-iii/

/*
PROBLEM:
Select the first year of every product sold along with quantity and price.
For each product, return the product_id, first_year, quantity, and price for the first year of sale.

TABLES:
- Sales (sale_id, product_id, year, quantity, price)
- Product (product_id, product_name)

EXPECTED OUTPUT:
| product_id | first_year | quantity | price |
|------------|------------|----------|-------|
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |

EXAMPLE:
Product 100:
  - Sale in 2008: quantity=10, price=5000 ← FIRST YEAR
  - Sale in 2009: quantity=12, price=5000 (excluded, not first year)
  - Result: Show 2008 data only

Product 200:
  - Sale in 2011: quantity=15, price=9000 ← FIRST YEAR (only sale)
  - Result: Show 2011 data
*/

-- STEP 1: Subquery to identify first year of sale for each product
-- Use MIN(year) grouped by product_id to find earliest sale year per product
-- This creates pairs of (product_id, first_year)

-- STEP 2: Filter main table to include only first-year sales
-- WHERE with IN clause matches (product_id, year) tuples
-- Only rows matching the first year for each product are included

-- STEP 3: Select required columns
-- product_id: Product identifier
-- year AS first_year: Rename year column to first_year
-- quantity: Quantity sold in first year
-- price: Price in first year

SELECT 
    product_id,                                              -- Product identifier
    year AS first_year,                                      -- First year of sale (renamed column)
    quantity,                                                -- Quantity sold in first year
    price                                                    -- Price in first year
FROM Sales
WHERE (product_id, year) IN (                                -- Filter: only first-year sales
    SELECT 
        product_id, 
        MIN(year)                                            -- Find earliest year per product
    FROM Sales
    GROUP BY product_id                                      -- One result per product
);

/*
WHY EACH PART:
- Subquery with MIN(year): Finds the first sale year for each product
  - Example: Product 100 has sales in 2008, 2009 → MIN = 2008
  
- GROUP BY product_id: Ensures one first year per product
  - Without this, MIN would return single global minimum (incorrect)

- (product_id, year) IN (...): Tuple comparison filters exact matches
  - Checks if BOTH product_id AND year match the subquery results
  - Example: (100, 2008) ✓ matches, (100, 2009) ✗ doesn't match

- year AS first_year: Renames column for clarity in output
  - Alias makes output more descriptive

HOW IT WORKS (Product 100):
1. Subquery finds: (100, 2008)
2. Main query checks each row:
   - Row with (100, 2008) ✓ included
   - Row with (100, 2009) ✗ excluded
3. Result: Only first-year sale data is returned

KEY TECHNIQUE:
- Subquery in WHERE with tuple comparison
- Same pattern as "first login" or "first order" problems
- Filters to "first occurrence" based on MIN of a date/year column

CONCEPTS USED:
- Subquery in WHERE clause
- MIN() aggregate function
- GROUP BY
- IN clause with tuple comparison
- Column alias with AS
- Filtering based on aggregated subquery results
*/

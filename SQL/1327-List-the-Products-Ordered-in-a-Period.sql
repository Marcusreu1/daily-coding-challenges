-- 1327. List the Products Ordered in a Period
-- Difficulty: Easy
-- https://leetcode.com/problems/list-the-products-ordered-in-a-period/

/*
PROBLEM:
Find products that have at least 100 units ordered in February 2020.
Return product_name and total units ordered in that period.

TABLES:
- Products (product_id PK, product_name, product_category)
- Orders (product_id, order_date, unit)
- unit: number of products ordered on order_date

EXPECTED OUTPUT:
+--------------------+--------+
| product_name       | unit   |
+--------------------+--------+
| Leetcode Solutions | 130    |
| Leetcode Kit       | 100    |
+--------------------+--------+

EXAMPLE:
Product 1 (Leetcode Solutions):
  - 2020-02-05: 60 units
  - 2020-02-10: 70 units
  - Total February 2020: 130 units ✓ (>= 100)

Product 2 (Jewels of Stringology):
  - 2020-02-11: 80 units
  - Total February 2020: 80 units ✗ (< 100)

Product 5 (Leetcode Kit):
  - 2020-02-25: 50 units
  - 2020-02-27: 50 units
  - Total February 2020: 100 units ✓ (>= 100)
*/

-- STEP 1: JOIN Products with Orders to get product names
-- Connects product_id to access product_name

-- STEP 2: Filter orders to February 2020 only
-- BETWEEN '2020-02-01' AND '2020-02-29' includes entire month

-- STEP 3: Group by product to sum units per product
-- GROUP BY product_id aggregates all orders for each product

-- STEP 4: Sum total units ordered per product
-- SUM(o.unit) adds up all units across multiple orders

-- STEP 5: Filter products with at least 100 units
-- HAVING filters aggregated results (after GROUP BY)

SELECT 
    p.product_name,
    SUM(o.unit) AS unit                                                          -- Total units in period
FROM Products p
JOIN Orders o ON p.product_id = o.product_id                                     -- Connect products to orders
WHERE o.order_date BETWEEN '2020-02-01' AND '2020-02-29'                        -- February 2020 only
GROUP BY p.product_id, p.product_name                                            -- Aggregate per product
HAVING SUM(o.unit) >= 100;                                                       -- At least 100 units

/*
WHY EACH PART:
- JOIN: Connects Orders to Products to get product_name
- WHERE order_date BETWEEN: Filters orders to February 2020 (before aggregation)
- GROUP BY product_id, product_name: Aggregates orders per product
- SUM(o.unit): Adds up units from multiple orders for same product
- HAVING SUM(o.unit) >= 100: Filters products after aggregation (not WHERE)
- Column aliases: p.product_name for clarity, o.unit for table reference

WHY GROUP BY includes product_name:
- product_id uniquely identifies products (sufficient for grouping)
- product_name is in SELECT but not aggregated (must be in GROUP BY)
- MySQL requires non-aggregated SELECT columns in GROUP BY
- Functional dependency: product_id determines product_name

WHY HAVING (not WHERE):
- WHERE filters rows BEFORE aggregation
- HAVING filters groups AFTER aggregation
- SUM(o.unit) is aggregate function (only available after GROUP BY)
- Cannot use WHERE SUM(o.unit) >= 100 (syntax error)

DATE FILTERING:
- BETWEEN '2020-02-01' AND '2020-02-29': Inclusive on both ends
- Covers all 29 days of February 2020 (leap year)
- Alternative: DATE_FORMAT(order_date, '%Y-%m') = '2020-02'
- Alternative: YEAR(order_date) = 2020 AND MONTH(order_date) = 2

KEY TECHNIQUE:
- WHERE for row filtering (before aggregation)
- HAVING for aggregate filtering (after GROUP BY)
- SUM with GROUP BY for totals per category
- Date range filtering with BETWEEN

ALTERNATIVE APPROACH (subquery):
SELECT 
    p.product_name,
    feb_orders.total_unit AS unit
FROM Products p
JOIN (
    SELECT product_id, SUM(unit) AS total_unit
    FROM Orders
    WHERE order_date BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY product_id
    HAVING SUM(unit) >= 100
) feb_orders ON p.product_id = feb_orders.product_id;

-- Aggregates in subquery, then joins with Products
-- More explicit but more verbose

EDGE CASES:
- Product with no orders in February: Not included (INNER JOIN filters out) ✓
- Product with exactly 100 units: Included (>= 100) ✓
- Product with orders in multiple months: Only February counted ✓
- Multiple orders on same date: All summed correctly ✓
- Product with 99 units: Excluded by HAVING ✓
- Product not in Orders table: Not included (INNER JOIN) ✓

CONCEPTS USED:
- INNER JOIN
- WHERE for date filtering
- BETWEEN for date ranges
- GROUP BY with multiple columns
- SUM() aggregate function
- HAVING for aggregate filtering
- Difference between WHERE and HAVING
*/

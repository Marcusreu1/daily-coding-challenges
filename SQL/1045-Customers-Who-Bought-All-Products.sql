-- 1045. Customers Who Bought All Products
-- Difficulty: Medium
-- https://leetcode.com/problems/customers-who-bought-all-products/

/*
PROBLEM:
Find all customers who bought all the products in the Product table.
Return the customer_id of customers who purchased every product at least once.

TABLES:
- Customer (customer_id, product_key)
- Product (product_key)

EXPECTED OUTPUT:
| customer_id |
|-------------|
| 1           |
| 3           |

EXAMPLE:
Product table (all available products):
| product_key |
|-------------|
| 5           |
| 6           |

Customer table (purchases):
| customer_id | product_key |
|-------------|-------------|
| 1           | 5           |
| 2           | 6           |
| 1           | 6           |
| 3           | 5           |
| 3           | 6           |
| 1           | 6           |

Analysis:
Total products available: 2 (products 5 and 6)

Customer 1:
  - Bought: 5, 6, 6 (duplicate purchase of 6)
  - Distinct products: {5, 6} = 2 products ✓ Bought ALL

Customer 2:
  - Bought: 6
  - Distinct products: {6} = 1 product ✗ Missing product 5

Customer 3:
  - Bought: 5, 6
  - Distinct products: {5, 6} = 2 products ✓ Bought ALL

Result: Customers 1 and 3 bought all products
*/

-- STEP 1: Filter to valid products only
-- WHERE product_key IN (...) ensures we only count products that exist in Product table
-- Prevents counting invalid/deleted products

-- STEP 2: Group by customer
-- GROUP BY customer_id aggregates all purchases per customer

-- STEP 3: Count distinct products per customer
-- COUNT(DISTINCT product_key) counts unique products each customer bought
-- DISTINCT is crucial: buying same product twice counts as 1

-- STEP 4: Compare to total products available
-- Subquery counts total distinct products in Product table
-- HAVING filters to customers whose distinct product count matches total

SELECT customer_id                                           -- Customer who bought all products
FROM Customer
WHERE product_key IN (                                       -- Filter: only valid products
    SELECT product_key FROM Product
)
GROUP BY customer_id                                         -- Group purchases by customer
HAVING COUNT(DISTINCT product_key) = (                       -- Count distinct products bought
    SELECT COUNT(DISTINCT product_key)                       -- Must equal total products available
    FROM Product
);

/*
WHY EACH PART:
- WHERE product_key IN (SELECT product_key FROM Product):
  Filters out invalid product_keys that might exist in Customer but not in Product
  - Product table: {5, 6}
  - Customer buys: {5, 6, 99}
  - WHERE clause removes 99 (not a valid product)
  - Without this: Could incorrectly count non-existent products
  
- GROUP BY customer_id: Collapses all purchases per customer
  - Customer 1: (1, 5), (1, 6), (1, 6) → becomes 1 group
  - Customer 2: (2, 6) → becomes 1 group
  - Customer 3: (3, 5), (3, 6) → becomes 1 group
  
- COUNT(DISTINCT product_key): Counts unique products per customer
  - Customer 1: products {5, 6} → COUNT = 2
  - Customer 2: products {6} → COUNT = 1
  - Customer 3: products {5, 6} → COUNT = 2
  - DISTINCT handles duplicate purchases (customer 1 bought product 6 twice)
  
- Subquery (SELECT COUNT(DISTINCT product_key) FROM Product):
  Calculates total number of products available
  - Product table: {5, 6} → COUNT = 2
  - This is the "target" number customers must reach
  
- HAVING ... = (subquery):
  Filters to customers who bought ALL products
  - Customer 1: 2 = 2 ✓ (bought all)
  - Customer 2: 1 ≠ 2 ✗ (missing products)
  - Customer 3: 2 = 2 ✓ (bought all)

KEY CONCEPT - RELATIONAL DIVISION (Find ALL Pattern):
This is a classic "division" operation in relational algebra.
Pattern: Find entities that have ALL items from a set.

Generic structure:
SELECT entity_id
FROM Transactions
WHERE item IN (SELECT item FROM RequiredSet)    -- Filter valid items
GROUP BY entity_id
HAVING COUNT(DISTINCT item) = (                 -- Count must match total
    SELECT COUNT(DISTINCT item) FROM RequiredSet
);

Real-world applications:
- Students who passed ALL required courses
- Users who visited ALL pages
- Employees who completed ALL training modules
- Customers who bought ALL products (this problem)

WHY COUNT(DISTINCT) IS CRUCIAL:
Without DISTINCT:
- Customer 1 buys: 5, 6, 6 → COUNT = 3
- Total products: 2
- 3 ≠ 2 → Customer 1 incorrectly excluded ✗

With DISTINCT:
- Customer 1 buys: 5, 6, 6 → COUNT(DISTINCT) = 2
- Total products: 2
- 2 = 2 → Customer 1 correctly included ✓

ALTERNATIVE APPROACHES:
1. Using LEFT JOIN with NULL check:
   SELECT c.customer_id
   FROM (
       SELECT customer_id, COUNT(DISTINCT product_key) AS bought_count
       FROM Customer
       GROUP BY customer_id
   ) c
   CROSS JOIN (
       SELECT COUNT(DISTINCT product_key) AS total_count
       FROM Product
   ) p
   WHERE c.bought_count = p.total_count;

2. Using INNER JOIN + GROUP BY:
   SELECT c.customer_id
   FROM Customer c
   INNER JOIN Product p ON c.product_key = p.product_key
   GROUP BY c.customer_id
   HAVING COUNT(DISTINCT c.product_key) = (
       SELECT COUNT(*) FROM Product
   );

EDGE CASES:
- Customer bought same product multiple times: COUNT(DISTINCT) handles ✓
- Customer bought products not in Product table: WHERE IN filters out ✓
- Customer bought no products: COUNT = 0, not included ✓
- Product table empty: No customer can buy all (result: empty) ✓
- Only 1 product exists: Customers who bought it are returned ✓

EXECUTION ORDER:
1. Subquery calculates total products: COUNT = 2
2. WHERE filters valid product purchases
3. GROUP BY groups by customer
4. COUNT(DISTINCT) counts unique products per customer
5. HAVING filters customers matching total count

CONCEPTS USED:
- Relational Division pattern (Find ALL)
- Subquery in WHERE clause (filtering)
- Subquery in HAVING clause (comparison)
- GROUP BY for aggregation
- COUNT(DISTINCT) to count unique values
- IN operator for set membership
*/

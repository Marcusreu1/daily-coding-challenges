-- 1174. Immediate Food Delivery II
-- Difficulty: Medium
-- https://leetcode.com/problems/immediate-food-delivery-ii/ 

/*
PROBLEM:
Calculate the percentage of first orders that are immediate orders.
Round to 2 decimal places.

Definitions:
- Immediate order: order_date = customer_pref_delivery_date (customer wants it same day)
- Scheduled order: order_date ≠ customer_pref_delivery_date (customer wants it later)
- First order: The earliest order (MIN order_date) for each customer

TABLES:
- Delivery (delivery_id, customer_id, order_date, customer_pref_delivery_date)

EXPECTED OUTPUT:
| immediate_percentage |
|----------------------|
| 50.00                |

EXAMPLE:
Customer 1:
  - Order 1: 2019-08-01 → pref 2019-08-02 (scheduled) ← FIRST ORDER
  - Order 3: 2019-08-11 → pref 2019-08-12 (scheduled)

Customer 2:
  - Order 2: 2019-08-02 → pref 2019-08-02 (immediate) ← FIRST ORDER ✓
  - Order 6: 2019-08-11 → pref 2019-08-13 (scheduled)

Customer 3:
  - Order 5: 2019-08-21 → pref 2019-08-22 (scheduled) ← FIRST ORDER
  - Order 4: 2019-08-24 → pref 2019-08-24 (immediate)

First orders: 3 total, 1 immediate → (1/3) * 100 = 33.33%
*/

-- STEP 1: Subquery to identify first order date for each customer
-- Use MIN(order_date) grouped by customer_id to find earliest order per customer
-- This creates a list of (customer_id, first_order_date) pairs

-- STEP 2: Filter main table to include only first orders
-- Use WHERE with IN clause to match (customer_id, order_date) pairs
-- This ensures we only analyze each customer's first order

-- STEP 3: Count immediate orders among first orders
-- SUM(CASE WHEN...) counts rows where order_date = customer_pref_delivery_date
-- These are orders where customer wanted delivery same day

-- STEP 4: Calculate percentage
-- Divide immediate count by total first orders count
-- Multiply by 100.0 to convert to percentage (decimal division)

-- STEP 5: Round to 2 decimal places
-- ROUND(..., 2) formats result as required

SELECT 
    ROUND(                                                                       -- Round to 2 decimals
        SUM(CASE 
            WHEN order_date = customer_pref_delivery_date THEN 1                -- Count if immediate
            ELSE 0                                                               -- Don't count if scheduled
        END) * 100.0                                                             -- Convert to percentage
        / COUNT(*),                                                              -- Divide by total first orders
        2
    ) AS immediate_percentage
FROM Delivery
WHERE (customer_id, order_date) IN (                                             -- Filter: only first orders
    SELECT customer_id, MIN(order_date)                                          -- Subquery: find first order date
    FROM Delivery
    GROUP BY customer_id                                                         -- Per customer
);

/*
WHY EACH PART:
- Subquery with MIN(): Finds the earliest order_date for each customer
- GROUP BY customer_id: Ensures we get one first order date per customer
- (customer_id, order_date) IN (...): Filters to match exact (customer, date) pairs
- SUM(CASE WHEN...): Counts immediate orders (1 if true, 0 if false)
- COUNT(*): Counts total first orders after filtering
- * 100.0: Converts proportion to percentage with decimal division
- ROUND(..., 2): Formats result to 2 decimal places

KEY TECHNIQUE:
- Subquery in WHERE clause: Allows filtering based on aggregated data (MIN per group)
- Tuple comparison with IN: (a, b) IN ((1, 2), (3, 4)) checks if pair matches any in list
- This avoids needing window functions or complex joins

CONCEPTS USED:
- Subquery in WHERE clause
- MIN() aggregate function
- GROUP BY
- IN clause with tuple comparison
- SUM() with CASE for conditional counting
- COUNT() for total rows
- Percentage calculation with decimal division
- ROUND()
*/

-- 1484. Group Sold Products By The Date
-- Difficulty: Easy
-- https://leetcode.com/problems/group-sold-products-by-the-date/

/*
PROBLEM:
For each date, find:
1. Number of distinct products sold
2. Names of distinct products, ordered lexicographically and separated by commas

Order result by sell_date.

TABLES:
- Activities (sell_date, product)
- No primary key (duplicate rows possible)

EXPECTED OUTPUT:
+------------+----------+------------------------------+
| sell_date  | num_sold | products                     |
+------------+----------+------------------------------+
| 2020-05-30 | 3        | Basketball,Headphone,T-Shirt |
| 2020-06-01 | 2        | Bible,Pencil                 |
| 2020-06-02 | 1        | Mask                         |
+------------+----------+------------------------------+

EXAMPLE:
2020-05-30: Products [Headphone, Basketball, T-Shirt]
  - num_sold: 3 distinct products
  - products: "Basketball,Headphone,T-Shirt" (alphabetically sorted)

2020-06-02: Products [Mask, Mask]
  - num_sold: 1 (duplicates counted once)
  - products: "Mask"
*/

-- STEP 1: Group activities by sell_date
-- Each date becomes one row in the result

-- STEP 2: Count distinct products per date
-- COUNT(DISTINCT product) handles duplicate products on same date

-- STEP 3: Concatenate distinct products into comma-separated list
-- GROUP_CONCAT combines multiple values into single string
-- DISTINCT removes duplicate products before concatenation
-- ORDER BY product sorts alphabetically
-- SEPARATOR ',' specifies comma separator

-- STEP 4: Order final results by sell_date
-- ORDER BY ensures chronological output

SELECT 
    sell_date,
    COUNT(DISTINCT product) AS num_sold,                                        -- Count unique products
    GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') AS products   -- Ordered comma-separated list
FROM Activities
GROUP BY sell_date                                                              -- One row per date
ORDER BY sell_date;                                                             -- Chronological order

/*
WHY EACH PART:
- GROUP BY sell_date: Aggregates all products sold on same date
- COUNT(DISTINCT product): Counts unique products (ignores duplicates)
- GROUP_CONCAT: Combines multiple product names into single string
- DISTINCT in GROUP_CONCAT: Removes duplicate products before concatenation
- ORDER BY product: Sorts products alphabetically within each date
- SEPARATOR ',': Specifies comma as delimiter (default is also comma)
- AS num_sold/products: Names output columns as required
- ORDER BY sell_date: Sorts result rows by date

GROUP_CONCAT SYNTAX:
GROUP_CONCAT([DISTINCT] column 
             [ORDER BY column [ASC|DESC]]
             [SEPARATOR 'delimiter'])

- DISTINCT: Remove duplicates before concatenating
- ORDER BY: Sort values before concatenating
- SEPARATOR: Custom delimiter (default is comma)

HOW IT WORKS (example for 2020-05-30):
Rows for 2020-05-30: [Headphone, Basketball, T-Shirt]

COUNT(DISTINCT product):
  Unique products: [Headphone, Basketball, T-Shirt]
  Count: 3

GROUP_CONCAT(DISTINCT product ORDER BY product):
  Unique products: [Headphone, Basketball, T-Shirt]
  After ORDER BY: [Basketball, Headphone, T-Shirt]
  Concatenated: "Basketball,Headphone,T-Shirt"

WHY DISTINCT IS NECESSARY:
Without DISTINCT:
Input: [Mask, Mask] on 2020-06-02
GROUP_CONCAT result: "Mask,Mask" ✗

With DISTINCT:
Input: [Mask, Mask] on 2020-06-02
GROUP_CONCAT result: "Mask" ✓

KEY TECHNIQUE:
- GROUP_CONCAT: Aggregate function that concatenates strings
- DISTINCT within aggregation: Removes duplicates before processing
- ORDER BY within GROUP_CONCAT: Controls sort order of concatenated values
- Combining COUNT(DISTINCT) with GROUP_CONCAT for summary statistics

EDGE CASES:
- Single product on date: Returns "ProductName" (no comma) ✓
- Multiple duplicate products: DISTINCT handles correctly ✓
- Same product on different dates: Each date groups separately ✓
- Empty date (no products): Won't appear (GROUP BY filters empty groups) ✓
- Products with special characters: Concatenated as-is ✓

CONCEPTS USED:
- GROUP BY aggregation
- COUNT(DISTINCT) for unique counting
- GROUP_CONCAT for string concatenation
- DISTINCT within GROUP_CONCAT
- ORDER BY within GROUP_CONCAT
- SEPARATOR clause
- ORDER BY for final result sorting
- Column aliasing
*/

-- 585. Investments in 2016
-- Difficulty: Medium
-- https://leetcode.com/problems/investments-in-2016/

/*
PROBLEM:
Calculate the sum of tiv_2016 for policyholders who meet BOTH conditions:
1. tiv_2015 is NOT unique (at least one other policyholder has same tiv_2015)
2. Location (lat, lon) IS unique (no other policyholder at same location)

Round result to 2 decimal places.

TABLES:
- Insurance (pid PK, tiv_2015, tiv_2016, lat, lon)

EXPECTED OUTPUT:
+----------+
| tiv_2016 |
+----------+
| 45.00    |
+----------+

EXAMPLE:
Policyholders:
pid 1: tiv_2015=10, location=(10,10), tiv_2016=5
pid 2: tiv_2015=20, location=(20,20), tiv_2016=20
pid 3: tiv_2015=10, location=(20,20), tiv_2016=30
pid 4: tiv_2015=10, location=(40,40), tiv_2016=40

tiv_2015 analysis:
- 10: Appears 3 times (pid 1,3,4) ✓ REPEATED
- 20: Appears 1 time (pid 2) ✗ UNIQUE

Location analysis:
- (10,10): Only pid 1 ✓ UNIQUE
- (20,20): pid 2 and 3 ✗ NOT UNIQUE
- (40,40): Only pid 4 ✓ UNIQUE

Qualifying policyholders:
- pid 1: tiv_2015 repeated ✓, location unique ✓ → Include (5)
- pid 2: tiv_2015 unique ✗ → Exclude
- pid 3: location not unique ✗ → Exclude
- pid 4: tiv_2015 repeated ✓, location unique ✓ → Include (40)

Result: 5 + 40 = 45.00
*/

-- STEP 1: First subquery finds repeated tiv_2015 values
-- GROUP BY tiv_2015 aggregates rows by investment value
-- HAVING COUNT(*) > 1 keeps only values appearing multiple times

-- STEP 2: Second subquery finds unique locations
-- GROUP BY lat, lon aggregates rows by location coordinates
-- HAVING COUNT(*) = 1 keeps only locations with exactly one policyholder

-- STEP 3: Main query filters and sums
-- WHERE with two conditions: repeated tiv_2015 AND unique location
-- (lat, lon) IN uses tuple matching for composite key
-- SUM(tiv_2016) aggregates qualifying investments
-- ROUND(..., 2) formats to 2 decimal places

SELECT 
    ROUND(SUM(tiv_2016), 2) AS tiv_2016                                         -- Sum and round to 2 decimals
FROM Insurance
WHERE 
    tiv_2015 IN (                                                                -- Condition 1: Repeated tiv_2015
        SELECT tiv_2015
        FROM Insurance
        GROUP BY tiv_2015                                                        -- Group by investment value
        HAVING COUNT(*) > 1                                                      -- Keep duplicates only
    )
    AND 
    (lat, lon) IN (                                                              -- Condition 2: Unique location
        SELECT lat, lon
        FROM Insurance
        GROUP BY lat, lon                                                        -- Group by coordinates
        HAVING COUNT(*) = 1                                                      -- Keep unique locations only
    );

/*
WHY EACH PART:
- First subquery: Identifies tiv_2015 values shared by multiple policyholders
- GROUP BY tiv_2015: Aggregates by investment value
- HAVING COUNT(*) > 1: Filters for values appearing at least twice (not unique)
- Second subquery: Identifies locations occupied by only one policyholder
- GROUP BY lat, lon: Aggregates by coordinate pair (composite key)
- HAVING COUNT(*) = 1: Filters for locations with exactly one policyholder (unique)
- (lat, lon) IN: Tuple comparison matches composite key in subquery
- tiv_2015 IN: Checks if value exists in set of repeated values
- AND: Both conditions must be true for inclusion
- SUM(tiv_2016): Aggregates investment values for qualifying rows
- ROUND(..., 2): Formats result to 2 decimal places

WHY TUPLE (lat, lon) IN:
- Location requires TWO columns (latitude and longitude)
- (lat, lon) IN (...) matches both coordinates simultaneously
- Alternative would be JOIN (more verbose, same result)

WHY GROUP BY + HAVING pattern:
- GROUP BY aggregates rows by common value(s)
- HAVING filters groups (not individual rows)
- Allows counting occurrences: COUNT(*) = 1 (unique), COUNT(*) > 1 (duplicate)
- WHERE cannot filter by aggregated values (HAVING required)

KEY TECHNIQUE:
- Subquery with GROUP BY + HAVING: Find values by occurrence frequency
- Tuple matching: (col1, col2) IN (subquery) for composite keys
- Dual filtering: One condition for duplicates, one for uniqueness
- Aggregate after filter: SUM only qualifying rows

ALTERNATIVE APPROACH (with JOIN):
SELECT ROUND(SUM(i.tiv_2016), 2) AS tiv_2016
FROM Insurance i
JOIN (
    SELECT tiv_2015
    FROM Insurance
    GROUP BY tiv_2015
    HAVING COUNT(*) > 1
) AS repeated_tiv ON i.tiv_2015 = repeated_tiv.tiv_2015
JOIN (
    SELECT lat, lon
    FROM Insurance
    GROUP BY lat, lon
    HAVING COUNT(*) = 1
) AS unique_loc ON i.lat = unique_loc.lat AND i.lon = unique_loc.lon;

-- Uses JOINs instead of IN clauses (may perform differently)
-- Same logic, different syntax

EDGE CASES:
- All tiv_2015 values unique: No rows qualify (empty result, would need IFNULL)
- All locations duplicated: No rows qualify (empty result)
- Single policyholder: tiv_2015 is unique (excluded), location is unique (excluded)
- Multiple policyholders with same tiv_2015 at same location: Location not unique (excluded)
- NULL in lat or lon: Treated as distinct values (each NULL is unique)

CONCEPTS USED:
- Subquery in WHERE clause (two subqueries)
- GROUP BY (single column and composite)
- HAVING for group filtering
- COUNT(*) aggregate function
- Tuple matching with IN: (col1, col2) IN (...)
- SUM() aggregate function
- ROUND() for decimal formatting
- Multiple AND conditions in WHERE
*/

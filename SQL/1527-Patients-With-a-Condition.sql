-- 1527. Patients With a Condition
-- Difficulty: Easy
-- https://leetcode.com/problems/patients-with-a-condition/

/*
PROBLEM:
Find all patients who have Type I Diabetes (any condition starting with prefix DIAB1).
The code DIAB1 can appear:
- At the beginning of the conditions string
- After a space (as a separate word)

TABLES:
- Patients (patient_id PK, patient_name, conditions)
- conditions contains 0 or more code words separated by spaces

EXPECTED OUTPUT:
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 2          | Alice        | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
| 5          | Alain        | DIAB1        |
+------------+--------------+--------------+

EXAMPLE:
"DIAB100 MYOP" → Starts with DIAB1 ✓
"DIAB201" → Starts with DIAB2, not DIAB1 ✗
"ACNE DIAB100" → Contains " DIAB1" after space ✓
"DIAB1" → Exactly DIAB1 ✓
"XDIAB100" → DIAB1 not at word boundary ✗
*/

-- STEP 1: Check if conditions starts with DIAB1
-- Pattern 'DIAB1%' matches strings beginning with DIAB1

-- STEP 2: Check if conditions contains DIAB1 after a space
-- Pattern '% DIAB1%' matches space followed by DIAB1 (word boundary)

-- STEP 3: Combine both conditions with OR
-- Returns rows matching either pattern

SELECT *
FROM Patients
WHERE conditions LIKE 'DIAB1%'                                                   -- DIAB1 at start
   OR conditions LIKE '% DIAB1%';                                                -- DIAB1 after space

/*
WHY EACH PART:
- LIKE 'DIAB1%': Matches strings starting with DIAB1 (% = any characters after)
- LIKE '% DIAB1%': Matches space + DIAB1 + anything (ensures word boundary)
- Space before DIAB1: Critical to avoid matching "XDIAB1" in middle of word
- %: Wildcard for zero or more characters
- OR: Combines both patterns (patient qualifies if either matches)
- SELECT *: Returns all columns as required

WHY SPACE IN '% DIAB1%':
- Without space: '% DIAB1%' would match "XDIAB100" (DIAB1 in middle of word) ✗
- With space: ' DIAB1' ensures DIAB1 starts a new word ✓
- Conditions are space-separated codes, so space = word boundary

LIKE WILDCARD PATTERNS:
- %: Matches any sequence of characters (0 or more)
- _: Matches exactly one character
- 'DIAB1%': DIAB1, DIAB100, DIAB1ABC (anything starting with DIAB1)
- '% DIAB1%': " DIAB1", " DIAB100" (space before DIAB1)

KEY TECHNIQUE:
- Pattern matching with LIKE and wildcards
- Word boundary detection using space
- Multiple patterns with OR for different positions

ALTERNATIVE APPROACH (single pattern):
SELECT *
FROM Patients
WHERE CONCAT(' ', conditions) LIKE '% DIAB1%';

-- Prepends space to conditions
-- Now '% DIAB1%' matches both beginning and after-space cases
-- Clever but less explicit than two separate conditions

EDGE CASES:
- "DIAB1" (exact match): Matched by 'DIAB1%' ✓
- "DIAB100 DIAB200": Matched by 'DIAB1%' (first code) ✓
- "XDIAB100": NOT matched (DIAB1 not at word boundary) ✓
- "DIAB201": NOT matched (starts with DIAB2, not DIAB1) ✓
- " DIAB100" (leading space): Matched by '% DIAB1%' ✓
- "ACNE DIAB100 MYOP": Matched by '% DIAB1%' ✓
- Empty conditions: NOT matched ✓
- Multiple DIAB1 codes: Matched (only need one occurrence) ✓

CONCEPTS USED:
- LIKE operator for pattern matching
- Wildcards: % (zero or more characters)
- OR operator for multiple conditions
- Word boundary detection with space
- String pattern matching
*/

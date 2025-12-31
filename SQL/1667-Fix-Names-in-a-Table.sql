-- 1667. Fix Names in a Table
-- Difficulty: Easy
-- https://leetcode.com/problems/fix-names-in-a-table/

/*
PROBLEM:
Fix the names so that only the first character is uppercase and the rest are lowercase.
Return result ordered by user_id.

TABLES:
- Users (user_id PK, name)
- name consists of lowercase and uppercase characters

EXPECTED OUTPUT:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | Alice |
| 2       | Bob   |
+---------+-------+

EXAMPLE:
Input: "aLice" → Output: "Alice" (first char upper, rest lower)
Input: "bOB" → Output: "Bob" (first char upper, rest lower)
*/

-- STEP 1: Extract first character and convert to uppercase
-- SUBSTRING(name, 1, 1) gets the first character
-- UPPER() converts it to uppercase

-- STEP 2: Extract remaining characters and convert to lowercase
-- SUBSTRING(name, 2) gets all characters from position 2 to end
-- LOWER() converts them to lowercase

-- STEP 3: Concatenate both parts
-- CONCAT() joins uppercase first char with lowercase remainder

-- STEP 4: Order by user_id
-- ORDER BY ensures consistent output ordering

SELECT 
    user_id,
    CONCAT(
        UPPER(SUBSTRING(name, 1, 1)),                                            -- First character uppercase
        LOWER(SUBSTRING(name, 2))                                                -- Remaining characters lowercase
    ) AS name
FROM Users
ORDER BY user_id;                                                                -- Sort by user ID

/*
WHY EACH PART:
- SUBSTRING(name, 1, 1): Extracts first character (position 1, length 1)
- SUBSTRING(name, 2): Extracts from position 2 to end (rest of string)
- UPPER(): Converts first character to uppercase
- LOWER(): Converts remaining characters to lowercase
- CONCAT(): Joins uppercase first char with lowercase rest
- ORDER BY user_id: Ensures predictable output order

WHY SUBSTRING (not other functions):
- SUBSTRING(string, start, length): Standard SQL function for extracting substrings
- Position starts at 1 (not 0) in SQL
- SUBSTRING(name, 2) without length parameter = "from position 2 to end"

KEY TECHNIQUE:
- String manipulation: Extract, transform, concatenate
- Case conversion: UPPER() and LOWER()
- Positional extraction: SUBSTRING with start position

EDGE CASES:
- Single character name: SUBSTRING(name, 2) returns empty string (CONCAT handles gracefully)
- Already correct format: Still processed (redundant but correct)
- All uppercase name: Converted correctly to proper case
- All lowercase name: First char capitalized correctly
- Empty name: Would return empty string (if allowed)

CONCEPTS USED:
- String functions: SUBSTRING, UPPER, LOWER, CONCAT
- Positional string extraction
- String concatenation
- ORDER BY
- Column aliasing
*/

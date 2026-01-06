-- 1517. Find Users With Valid E-Mails
-- Difficulty: Easy
-- https://leetcode.com/problems/find-users-with-valid-e-mails/

/*
PROBLEM:
Find users with valid emails.
A valid email has:
- Prefix name: Starts with a letter, contains only letters, digits, underscore, period, or dash
- Domain: Must be exactly '@leetcode.com' (case-sensitive)

TABLES:
- Users (user_id PK, name, mail)

EXPECTED OUTPUT:
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
+---------+-----------+-------------------------+

EXAMPLE:
Valid emails:
- "winston@leetcode.com" ✓ (starts with letter, valid characters)
- "bella-@leetcode.com" ✓ (dash before @ is allowed)
- "sally.come@leetcode.com" ✓ (period in prefix is allowed)

Invalid emails:
- "john00@gmail.com" ✗ (wrong domain)
- "#john@leetcode.com" ✗ (starts with #, not a letter)
- "john@leetcode.COM" ✗ (domain is case-sensitive, must be lowercase)
- "@leetcode.com" ✗ (no prefix before @)
- "123abc@leetcode.com" ✗ (starts with digit, not letter)
*/

-- STEP 1: Use REGEXP to validate email format
-- Pattern: ^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode\\.com$
-- ^ = start of string
-- [a-zA-Z] = must start with letter
-- [a-zA-Z0-9_.-]* = followed by zero or more valid characters
-- @leetcode\\.com = literal domain (\\. escapes the dot)
-- $ = end of string

-- STEP 2: Use LIKE BINARY for case-sensitive domain check
-- Ensures domain is lowercase '@leetcode.com' (not @leetcode.COM)
-- BINARY makes comparison case-sensitive

SELECT 
    user_id, 
    name, 
    mail
FROM Users
WHERE mail REGEXP '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode\\.com$'                    -- Validate email format
  AND mail LIKE BINARY '%@leetcode.com';                                        -- Case-sensitive domain check

/*
WHY EACH PART:
- REGEXP: Pattern matching with regular expressions
- ^: Anchors pattern to start of string (no characters before)
- [a-zA-Z]: Character class for uppercase or lowercase letters
- [a-zA-Z0-9_.-]*: Zero or more valid prefix characters (letters, digits, _, ., -)
- *: Zero or more occurrences of previous character class
- @leetcode\\.com: Literal domain string (\\. escapes dot)
- $: Anchors pattern to end of string (no characters after)
- LIKE BINARY: Case-sensitive pattern matching
- '%@leetcode.com': Ensures domain is lowercase (REGEXP alone is case-insensitive in MySQL)

REGEXP PATTERN BREAKDOWN:
^[a-zA-Z]           → Must start with letter (a-z or A-Z)
[a-zA-Z0-9_.-]*     → Followed by any number of:
                      - Letters (a-z, A-Z)
                      - Digits (0-9)
                      - Underscore (_)
                      - Period (.)
                      - Dash (-)
@leetcode\\.com$    → Must end with @leetcode.com

WHY LIKE BINARY:
- REGEXP in MySQL is case-insensitive by default
- '@leetcode.com' and '@leetcode.COM' both match REGEXP
- LIKE BINARY forces case-sensitive comparison
- Ensures only lowercase domain is accepted

REGEX SPECIAL CHARACTERS:
- ^: Start of string anchor
- $: End of string anchor
- []: Character class (matches any character inside)
- *: Zero or more occurrences
- \\.: Escaped period (literal dot, not wildcard)
- |: OR operator (not used here)
- (): Grouping (not used here)

KEY TECHNIQUE:
- REGEXP for complex pattern validation
- Character classes for allowed characters
- Anchors (^ and $) to match entire string
- Escaping special characters (\\.)
- LIKE BINARY for case-sensitive matching

EDGE CASES:
- Email starts with digit: "123@leetcode.com" ✗ (must start with letter)
- Email starts with special char: "_test@leetcode.com" ✗ (must start with letter)
- Wrong domain: "test@gmail.com" ✗ (not @leetcode.com)
- Uppercase domain: "test@leetcode.COM" ✗ (case-sensitive)
- Mixed case domain: "test@Leetcode.com" ✗ (must be all lowercase)
- No prefix: "@leetcode.com" ✗ (must have prefix)
- Special chars in prefix: "te$t@leetcode.com" ✗ ($ not allowed)
- Valid special chars: "a_b.c-d@leetcode.com" ✓ (_, ., - allowed)

CONCEPTS USED:
- Regular expressions (REGEXP)
- Character classes [a-zA-Z]
- Quantifiers (*) 
- Anchors (^, $)
- Escaping special characters
- LIKE BINARY for case-sensitive matching
- Pattern validation
*/

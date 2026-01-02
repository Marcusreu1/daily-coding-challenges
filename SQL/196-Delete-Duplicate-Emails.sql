-- 196. Delete Duplicate Emails
-- Difficulty: Easy
-- https://leetcode.com/problems/delete-duplicate-emails/

/*
PROBLEM:
Delete all duplicate emails from Person table, keeping only the row with the smallest id for each unique email.
This is a DELETE operation (modifies the table, not a SELECT query).

TABLES:
- Person (id PK, email)

EXPECTED OUTPUT (table after DELETE):
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+

EXAMPLE:
Before DELETE:
id=1: john@example.com
id=2: bob@example.com
id=3: john@example.com (duplicate)

After DELETE:
id=1: john@example.com (kept, smallest id)
id=2: bob@example.com
id=3: DELETED (larger id for john@example.com)
*/

-- STEP 1: Self JOIN to compare rows with same email
-- p1 and p2 are aliases for the same Person table
-- JOIN condition: p1.email = p2.email finds matching emails

-- STEP 2: Filter to identify duplicates to delete
-- WHERE p1.id > p2.id means p1 has larger id (is the duplicate to remove)
-- For each email, keeps the row with smallest id

-- STEP 3: DELETE statement removes matching rows
-- DELETE p1 specifies which table alias to delete from
-- Only rows where p1.id > p2.id are deleted

DELETE p1
FROM Person p1
INNER JOIN Person p2 ON p1.email = p2.email                                     -- Match rows with same email
WHERE p1.id > p2.id;                                                             -- Delete rows with larger id

/*
WHY EACH PART:
- DELETE p1: Specifies to delete rows from p1 alias (not p2)
- FROM Person p1: First instance of table (rows to potentially delete)
- INNER JOIN Person p2: Second instance of same table (for comparison)
- ON p1.email = p2.email: Matches rows with duplicate emails
- WHERE p1.id > p2.id: Keeps smaller id, deletes larger id
- Self JOIN: Allows comparing each row with other rows in same table

HOW IT WORKS (example):
Person table:
| id | email            |
|----|------------------|
| 1  | john@example.com |
| 3  | john@example.com |

JOIN result (before WHERE):
| p1.id | p1.email         | p2.id | p2.email         |
|-------|------------------|-------|------------------|
| 1     | john@example.com | 1     | john@example.com | ← Same row, id not >
| 1     | john@example.com | 3     | john@example.com | ← p1.id < p2.id (skip)
| 3     | john@example.com | 1     | john@example.com | ← p1.id > p2.id (DELETE) ✓
| 3     | john@example.com | 3     | john@example.com | ← Same row, id not >

After WHERE p1.id > p2.id:
- Row with id=3 is deleted (p1.id=3 > p2.id=1)
- Row with id=1 remains (smallest id for john@example.com)

KEY TECHNIQUE:
- Self JOIN with DELETE: Compare rows in same table
- DELETE with table alias: Specify which rows to remove
- id comparison: p1.id > p2.id keeps minimum id per group

ALTERNATIVE APPROACH (with subquery):
DELETE FROM Person
WHERE id NOT IN (
    SELECT MIN(id)
    FROM Person
    GROUP BY email
);

-- Subquery finds smallest id for each email
-- DELETE removes all ids NOT in that list
-- Note: Some databases require derived table wrapper

WHY SELF JOIN (not just GROUP BY):
- DELETE cannot use GROUP BY directly
- Self JOIN allows row-by-row comparison
- WHERE p1.id > p2.id identifies which specific rows to delete

EDGE CASES:
- No duplicates: No rows match WHERE condition (nothing deleted) ✓
- All emails unique: No JOIN matches with different ids (nothing deleted) ✓
- Multiple duplicates (id 1,2,3 same email): Deletes 2 and 3, keeps 1 ✓
- Two duplicates with ids 5,10: Deletes 10, keeps 5 ✓
- Same email, consecutive ids: Works correctly (keeps smallest) ✓

CONCEPTS USED:
- DELETE statement
- Self JOIN (table joined with itself)
- INNER JOIN
- Table aliases (p1, p2)
- WHERE with comparison condition
- DELETE with JOIN syntax
*/

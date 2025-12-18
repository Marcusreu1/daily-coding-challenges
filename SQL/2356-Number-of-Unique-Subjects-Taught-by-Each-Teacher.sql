-- 2356. Number of Unique Subjects Taught by Each Teacher
-- Difficulty: Easy
-- https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/

/*
PROBLEM:
Report the number of unique subjects each teacher teaches at the university.
Return the result in any order.

TABLES:
- Teacher (teacher_id, subject_id, dept_id)

EXPECTED OUTPUT:
| teacher_id | cnt |
|------------|-----|
| 1          | 2   |
| 2          | 4   |

EXAMPLE:
Teacher 1:
  - Teaches subject 2 in dept 3
  - Teaches subject 2 in dept 4 (same subject, different department)
  - Teaches subject 3 in dept 3
  - Unique subjects: 2, 3 → Total: 2

Teacher 2:
  - Teaches subjects 1, 2, 3, 4 in dept 1
  - Unique subjects: 1, 2, 3, 4 → Total: 4
*/

-- STEP 1: Use COUNT(DISTINCT subject_id) to count unique subjects
-- DISTINCT ensures each subject is counted only once per teacher
-- Even if teacher teaches same subject in multiple departments, count it once

-- STEP 2: GROUP BY teacher_id to get one result per teacher
-- This aggregates all rows for each teacher into a single count

SELECT 
    teacher_id,                                  -- Teacher identifier
    COUNT(DISTINCT subject_id) AS cnt            -- Count unique subjects per teacher
FROM Teacher
GROUP BY teacher_id;                             -- One row per teacher

/*
WHY EACH PART:
- COUNT(DISTINCT subject_id): Counts only unique subject IDs for each teacher
- DISTINCT: Eliminates duplicate subjects (same subject in different departments)
- GROUP BY teacher_id: Aggregates all teaching records per teacher
- No need to consider dept_id: Problem only asks for unique subjects, not departments

EXAMPLE WALKTHROUGH (Teacher 1):
- Row 1: subject_id = 2
- Row 2: subject_id = 2 (duplicate, ignored by DISTINCT)
- Row 3: subject_id = 3
- COUNT(DISTINCT) = 2 (subjects 2 and 3)

CONCEPTS USED:
- COUNT(DISTINCT column): Count unique values
- GROUP BY: Aggregate data per group
- Aggregate functions with DISTINCT
*/

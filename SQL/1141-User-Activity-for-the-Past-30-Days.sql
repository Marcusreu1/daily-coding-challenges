-- 1141. User Activity for the Past 30 Days I
-- Difficulty: Easy
-- https://leetcode.com/problems/user-activity-for-the-past-30-days-i/

/*
PROBLEM:
Find the daily active user count for a period of 30 days ending on 2019-07-27 (inclusive).
A user is active on a day if they have at least one activity on that day.

TABLES:
- Activity (user_id, session_id, activity_date, activity_type)

EXPECTED OUTPUT:
| day        | active_users |
|------------|--------------|
| 2019-07-20 | 2            |
| 2019-07-21 | 2            |

EXAMPLE:
Date range: 2019-06-28 to 2019-07-27 (30 days ending on 2019-07-27)

2019-07-20:
  - User 1: has activities (open_session, scroll_down, end_session)
  - User 2: has activity (open_session)
  - Active users: 2 (users 1 and 2)

2019-07-21:
  - User 2: has activities (send_message, end_session)
  - User 3: has activities (open_session, send_message, end_session)
  - Active users: 2 (users 2 and 3)

2019-06-25:
  - User 4: has activities
  - NOT included: DATEDIFF('2019-07-27', '2019-06-25') = 32 days (exceeds 30-day window)
*/

-- STEP 1: Filter dates within 30-day window before 2019-07-27
-- Use DATEDIFF to calculate days between reference date and activity_date
-- DATEDIFF < 30: ensures activity is within last 30 days
-- DATEDIFF >= 0: ensures activity is not in the future (on or before 2019-07-27)

-- STEP 2: Count DISTINCT users per day
-- COUNT(DISTINCT user_id) counts each user only once per day
-- Even if user has multiple activities on same day, count as 1 active user

-- STEP 3: GROUP BY activity_date to get counts per day
-- Each row in result represents one day with its active user count

SELECT 
    activity_date AS day,                                    -- Date of activity
    COUNT(DISTINCT user_id) AS active_users                  -- Count unique users per day
FROM Activity
WHERE DATEDIFF('2019-07-27', activity_date) < 30             -- Within 30 days before 2019-07-27
  AND DATEDIFF('2019-07-27', activity_date) >= 0             -- Not in the future
GROUP BY activity_date;                                      -- One result per day

/*
WHY EACH PART:
- DATEDIFF('2019-07-27', activity_date): Calculates days between dates
  - Returns positive number if activity_date is before 2019-07-27
  - Example: DATEDIFF('2019-07-27', '2019-07-26') = 1 day
  - Example: DATEDIFF('2019-07-27', '2019-06-28') = 29 days
  
- < 30: Filters to last 30 days (0 to 29 days difference)
  - Day 0 = 2019-07-27 (today) ✓
  - Day 29 = 2019-06-28 (29 days ago) ✓
  - Day 30 = 2019-06-27 (30 days ago) ✗ excluded
  
- >= 0: Excludes future dates (activities after 2019-07-27)

- COUNT(DISTINCT user_id): Counts unique users per day
  - User with 3 activities on same day = 1 active user
  - Without DISTINCT would count as 3 (incorrect)

- GROUP BY activity_date: Aggregates all activities per day

ALTERNATIVE APPROACH:
Could also use BETWEEN for date filtering:
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
Both approaches are valid.

CONCEPTS USED:
- DATEDIFF() for date comparison
- COUNT(DISTINCT column) to count unique values
- WHERE clause for filtering
- GROUP BY for aggregation by date
- Column alias with AS
*/

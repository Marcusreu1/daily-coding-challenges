-- 550. Game Play Analysis IV
-- Difficulty: Medium
-- https://leetcode.com/problems/game-play-analysis-iv/

/*
PROBLEM:
Calculate the fraction of players who logged in the day immediately following their first login.
Round to 2 decimal places.

Definitions:
- First login: The earliest event_date for each player
- Consecutive login: Player logged in on (first_login + 1 day)

TABLES:
- Activity (player_id, device_id, event_date, games_played)

EXPECTED OUTPUT:
| fraction |
|----------|
| 0.33     |

EXAMPLE:
Player 1:
  - First login: 2016-03-01
  - Has login on 2016-03-02? YES ✓ (consecutive)

Player 2:
  - First login: 2017-06-25
  - Has login on 2017-06-26? NO ✗

Player 3:
  - First login: 2016-03-02
  - Has login on 2016-03-03? NO ✗

Result: 1 out of 3 players = 1/3 = 0.33
*/

-- STEP 1: Subquery to find first login date for each player
-- Use MIN(event_date) grouped by player_id to get earliest login per player
-- This creates a derived table with (player_id, first_login) pairs

-- STEP 2: LEFT JOIN with Activity to find next-day logins
-- Join condition 1: Same player_id
-- Join condition 2: event_date equals first_login + 1 day
-- LEFT JOIN ensures all players are included (even without consecutive login)

-- STEP 3: Use DATE_ADD to calculate next day
-- DATE_ADD(first_login, INTERVAL 1 DAY) adds exactly one day to the date
-- This is the expected date for consecutive login

-- STEP 4: Count players with consecutive logins
-- COUNT(next_day.event_date) counts only NOT NULL values
-- These are players who have a login record on the next day

-- STEP 5: Count total players
-- COUNT(first.player_id) counts all players from subquery
-- This gives the denominator for the fraction

-- STEP 6: Calculate fraction and round
-- Divide consecutive by total, multiply by 1.0 for decimal division
-- ROUND(..., 2) formats to 2 decimal places

SELECT 
    ROUND(                                                                       -- Round to 2 decimals
        COUNT(next_day.event_date) * 1.0                                        -- Count players with consecutive login
        / COUNT(first.player_id),                                                -- Divide by total players
        2
    ) AS fraction
FROM (
    SELECT 
        player_id, 
        MIN(event_date) AS first_login                                           -- Find first login date per player
    FROM Activity
    GROUP BY player_id                                                           -- One result per player
) AS first                                                                       -- Subquery alias: first logins
LEFT JOIN Activity AS next_day                                                   -- Join with Activity again
  ON first.player_id = next_day.player_id                                        -- Match same player
  AND next_day.event_date = DATE_ADD(first.first_login, INTERVAL 1 DAY);        -- Match next day login

/*
WHY EACH PART:
- Subquery with MIN(): Identifies the first login date for each player
- GROUP BY player_id: Ensures one first login date per player
- LEFT JOIN: Includes all players, even those without next-day login (NULL)
- DATE_ADD(..., INTERVAL 1 DAY): Calculates the expected consecutive login date
- COUNT(next_day.event_date): Counts only NOT NULL (players with consecutive login)
- COUNT(first.player_id): Counts all players (denominator)
- * 1.0: Forces decimal division (avoids integer division)
- ROUND(..., 2): Formats result to 2 decimal places

WHY LEFT JOIN (not INNER):
- INNER JOIN would only show players WITH consecutive login (wrong denominator)
- LEFT JOIN shows ALL players, with NULL for those without consecutive login
- This allows correct calculation: some_players / all_players

KEY TECHNIQUE:
- Self JOIN: Joining Activity table with itself to compare different dates
- Subquery as table: Using query result as temporary table in FROM clause
- DATE_ADD: Date arithmetic to calculate next day
- COUNT with NULL handling: COUNT(column) ignores NULL values

CONCEPTS USED:
- Subquery in FROM clause (derived table)
- LEFT JOIN
- Self JOIN (table joined with itself)
- DATE_ADD() for date arithmetic
- MIN() aggregate function
- GROUP BY
- COUNT() with NULL handling
- Decimal division
- ROUND()
*/

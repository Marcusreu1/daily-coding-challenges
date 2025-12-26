-- 1341. Movie Rating
-- Difficulty: Medium
-- https://leetcode.com/problems/movie-rating/

/*
PROBLEM:
Return TWO results in a single output table:
1. Name of the user who has rated the most movies (COUNT). Tie-breaker: lexicographically smallest name.
2. Title of the movie with highest average rating in February 2020. Tie-breaker: lexicographically smallest title.

TABLES:
- Movies (movie_id PK, title)
- Users (user_id PK, name)
- MovieRating (movie_id, user_id, rating, created_at) - composite PK

EXPECTED OUTPUT:
+--------------+
| results      |
+--------------+
| Daniel       |
| Frozen 2     |
+--------------+

EXAMPLE:
Daniel: 3 ratings total (most active user)
Monica: 3 ratings total (tie, but "Monica" > "Daniel" lexicographically)
Maria: 2 ratings total

Frozen 2 in Feb 2020: (5+2)/2 = 3.5 average
Avengers in Feb 2020: (4+2)/2 = 3.0 average
Joker in Feb 2020: (3+4)/2 = 3.5 average (tie, but "Joker" > "Frozen 2" lexicographically)

Result: Daniel (most ratings), Frozen 2 (best avg in Feb 2020)
*/

-- QUERY 1: Find user with most ratings
-- JOIN Users with MovieRating to get user names
-- GROUP BY user to count ratings per user
-- ORDER BY count descending (most first), then name ascending (tie-breaker)
-- LIMIT 1 to get only the top user

-- QUERY 2: Find movie with best average rating in February 2020
-- JOIN Movies with MovieRating to get movie titles
-- Filter by February 2020 with BETWEEN
-- GROUP BY movie to calculate average rating per movie
-- ORDER BY average descending (best first), then title ascending (tie-breaker)
-- LIMIT 1 to get only the top movie

-- UNION ALL: Combine both results into single output
-- Both queries return one column named 'results'

(SELECT 
    name AS results                                                              -- User name as result
FROM Users u
JOIN MovieRating mr ON u.user_id = mr.user_id                                   -- Connect users to their ratings
GROUP BY u.user_id, u.name                                                       -- One row per user
ORDER BY COUNT(*) DESC, name ASC                                                 -- Most ratings first, then alphabetically
LIMIT 1)                                                                         -- Top user only

UNION ALL                                                                        -- Combine with second query

(SELECT 
    title AS results                                                             -- Movie title as result
FROM Movies m
JOIN MovieRating mr ON m.movie_id = mr.movie_id                                 -- Connect movies to their ratings
WHERE created_at BETWEEN '2020-02-01' AND '2020-02-29'                          -- Filter: February 2020 only
GROUP BY m.movie_id, m.title                                                     -- One row per movie
ORDER BY AVG(rating) DESC, title ASC                                             -- Best average first, then alphabetically
LIMIT 1);                                                                        -- Top movie only

/*
WHY EACH PART:
- Parentheses around each SELECT: Required when using ORDER BY/LIMIT before UNION
- AS results: Both queries must return same column name for UNION compatibility
- JOIN: Connect related tables to get user names and movie titles
- GROUP BY user_id/movie_id: Aggregate ratings per user/movie
- COUNT(*): Total number of ratings per user
- AVG(rating): Average rating score per movie
- ORDER BY with two columns: Primary sort + tie-breaker (lexicographical order)
- LIMIT 1: Get only the top result from each query
- BETWEEN for date range: Inclusive filter for February 2020
- UNION ALL: Faster than UNION (no duplicate removal needed)

WHY GROUP BY includes name/title:
- MySQL requires non-aggregated SELECT columns to be in GROUP BY
- Ensures proper grouping when fetching descriptive columns
- user_id/movie_id determines uniqueness, name/title are functional dependencies

WHY UNION ALL (not UNION):
- Results from two queries cannot overlap (user name vs movie title)
- UNION ALL is faster (skips duplicate check)
- No risk of eliminating valid results

KEY TECHNIQUE:
- UNION: Combine results from multiple independent queries
- Dual sorting: ORDER BY aggregate DESC, text ASC (best first, alphabetical tie-breaker)
- Date filtering: BETWEEN for inclusive range
- Column aliasing: Same alias in both queries for UNION compatibility

ALTERNATIVE APPROACH (separate queries):
-- Could use two separate queries and combine results in application layer
-- UNION is cleaner for single-query requirement

EDGE CASES:
- Multiple users with same rating count: Tie-breaker by name (ASC)
- Multiple movies with same average rating: Tie-breaker by title (ASC)
- No ratings in February 2020: Second query returns empty (UNION would show only first result)
- User with 0 ratings: Not included (INNER JOIN filters them out)

CONCEPTS USED:
- UNION ALL
- INNER JOIN (multiple tables)
- GROUP BY with multiple columns
- COUNT(*) aggregate
- AVG() aggregate
- ORDER BY with multiple columns (compound sorting)
- LIMIT
- Date filtering with BETWEEN
- Column aliasing
- Subquery parentheses with ORDER BY
*/

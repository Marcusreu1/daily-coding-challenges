# 843. Guess the Word
# Difficulty: Hard
# https://leetcode.com/problems/guess-the-word/

"""
PROBLEM:
You are given an array of unique strings `wordlist` where all words are 6 letters long.
One word from `wordlist` was chosen as a secret word.
You are given an interactive object `master` which has a method `master.guess(word)`.
When you call `master.guess(word)`, it returns an integer representing the number of 
exact matches (same letter in the exact same position) between your guessed word and the secret word.
You have 10 guesses to find the secret word.

EXAMPLES:
Input: secret = "acckzz", words = ["acckzz","ccbazz","eiowzz","abcczz"], allowedGuesses = 10
Output: You guessed the secret word correctly.

CONSTRAINTS:
- 1 <= words.length <= 100
- words[i].length == 6
- words[i] consists of lowercase English letters.
- All words[i] are unique.

FULL MINIMAX STRATEGY:
To defeat adversarial testcases that punish sequential or frequency-based guessing, 
we use a rigorous Minimax algorithm. We simulate guessing every single word in the 
original dictionary against our current pool of possible candidates. We group the 
remaining candidates by what the `master.guess()` output would be (0 to 6). 
We then select the word that MINIMIZES the size of the LARGEST group (the worst-case scenario).

VISUALIZATION (Minimax Partitioning):
Current 'possible' pool: 20 words.
If we guess word X (even if X is no longer in the pool):
- Output 0 matches: 12 words remain
- Output 1 match: 5 words remain
- Output 2 matches: 3 words remain
Max bucket (worst-case) = 12.

If we guess word Y:
- Output 0 matches: 6 words remain
- Output 1 match: 7 words remain
- Output 2 matches: 7 words remain
Max bucket (worst-case) = 7.

We pick word Y. Even if the adversarial judge gives us the worst possible output, 
we only have to deal with 7 words instead of 12.
"""

# STEP 1: Define a helper function to count positional matches between two words.
# STEP 2: Precompute a 2D matrix (M) storing the match counts between all word pairs to save time.
# STEP 3: Initialize the `possible` list with all word indices.
# STEP 4: Loop up to max_guesses (algorithm usually solves it in ~5-6 guesses).
# STEP 5: For EVERY word in the original list, simulate grouping the `possible` candidates into buckets based on match scores.
# STEP 6: Find the worst-case bucket size for each word.
# STEP 7: Keep the word that has the smallest worst-case bucket. Break ties by favoring words still in the `possible` pool.
# STEP 8: Call master.guess() with the best word. Exit if we win.
# STEP 9: Filter the `possible` pool by keeping only indices that have the exact same match score with our guess.

from typing import List

class Solution:
    def findSecretWord(self, wordlist: List[str], master: 'Master') -> None:
        
        # Helper to count exact matches
        def match(a: str, b: str) -> int:
            return sum(x == y for x, y in zip(a, b))

        n = len(wordlist)

        # Precompute match scores for all pairs to optimize performance
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                m = match(wordlist[i], wordlist[j])
                M[i][j] = m
                M[j][i] = m

        possible = list(range(n))
        max_guesses = 30  

        for _ in range(max_guesses):
            if not possible:
                return

            possible_set = set(possible)
            best = possible[0]
            best_score = float('inf')
            best_in_possible = True

            # Evaluate EVERY word in the original wordlist
            for i in range(n):
                buckets = [0] * 7  # Buckets for match scores 0 through 6
                
                # Simulate how guessing word 'i' partitions the currently possible words
                for j in possible:
                    buckets[M[i][j]] += 1

                score = max(buckets)  # The worst-case scenario (largest partition)
                in_possible = i in possible_set

                # We want to minimize the worst-case score.
                # Tie-breaker: If scores are equal, prefer a word that is actually still a valid candidate.
                if score < best_score or (score == best_score and in_possible and not best_in_possible):
                    best = i
                    best_score = score
                    best_in_possible = in_possible

            # Make the guess
            x = master.guess(wordlist[best])
            if x == 6:
                return

            # Strict Filtering: Keep only candidates that match the exact score returned by the API
            possible = [j for j in possible if M[best][j] == x]

"""
WHY EACH PART:
- M Matrix: Comparing strings is expensive. By precomputing the distances between all pairs once (O(N^2) operations), the inner loops just do O(1) array lookups.
- for i in range(n): Notice we iterate over the *entire* original list, not just `possible`. Sometimes guessing a word we know is wrong partitions the remaining candidates much more evenly than guessing a valid candidate.
- buckets: An array of size 7 represents the possible answers from master.guess() (0 to 6). We count how many candidates fall into each bucket.
- (score == best_score and in_possible and not best_in_possible): The tie-breaker logic. If an eliminated word and a valid candidate both partition the pool equally well, we should guess the valid candidate because it has a >0% chance of being the secret word and ending the game immediately.

HOW IT WORKS (Example Walkthrough):
1. Matrix Initialization: M[i][j] stores how similar word 'i' and word 'j' are.
2. Turn 1: Evaluates all 100 words. Finds the word that, in the absolute worst case, leaves the smallest number of candidates. Let's say it guesses word 45, and gets 0 matches.
3. Filtering: The `possible` list drops from 100 to, say, 15 indices.
4. Turn 2: Evaluates all 100 words again. It simulates guessing them against those 15 remaining indices. It finds the next optimal guess.
5. Win: The pool shrinks exponentially until 1 word remains. Usually completed in 5-6 guesses.

KEY TECHNIQUE:
- Strict Minimax Optimization: Minimizing the maximum subset size.
- Precomputed Lookup Table (Memoization): Trading space for significant time savings.
- Global Search Space Evaluation: Considering invalid options as valid tools for information gathering.

EDGE CASES:
- Adversarial Testcases: Perfectly neutralized. Because it calculates the worst possible outcome for every guess, the adversarial judge is forced into taking a path that still eliminates a massive chunk of the candidate pool.

TIME COMPLEXITY: 
- Precomputation: O(N^2 * L) where N is 100 and L is 6.
- Iteration: 10 guesses * O(N * P) where P is the size of the `possible` list.
- Total Time: ~O(N^2). Exceptionally fast.
SPACE COMPLEXITY: O(N^2) to store the 100x100 matrix M. Since N=100, this is negligible (10,000 integers).

CONCEPTS USED:
- Minimax Algorithm
- Game Theory (Adversarial Search)
- Precomputation / Memoization
- Array Partitioning
"""

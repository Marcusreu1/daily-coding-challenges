# 2063. Vowels of All Substrings
# Difficulty: Medium
# https://leetcode.com/problems/vowels-of-all-substrings/

"""
PROBLEM:
Given a string word, return the sum of the number of vowels ('a', 'e', 'i', 'o', and 'u') in every substring of word.
A substring is a contiguous (non-empty) sequence of characters within a string.

EXAMPLES:
Input: word = "aba" → Output: 6
Explanation: 
All possible substrings are: "a", "ab", "aba", "b", "ba", and "a".
- "a" has 1 vowel
- "ab" has 1 vowel
- "aba" has 2 vowels
- "b" has 0 vowels
- "ba" has 1 vowel
- "a" has 1 vowel
Total = 1 + 1 + 2 + 0 + 1 + 1 = 6.

Input: word = "abc" → Output: 3
Explanation: 
All possible substrings are: "a", "ab", "abc", "b", "bc", "c".
Only "a", "ab", and "abc" contain vowels (1 each). Total = 3.

CONSTRAINTS:
- 1 <= word.length <= 10^5
- word consists of lowercase English letters.

MATH RULES (CONTRIBUTION TECHNIQUE & COMBINATORICS):
Generating all substrings takes O(N^2) time, and counting vowels inside them takes O(N^3), which will result in a Time Limit Exceeded (TLE) error.
Instead of counting vowels per substring, we count the total substrings per vowel. This is known as the Contribution Technique.
For a character at index 'i' in a string of length 'N':
- A valid substring containing this character can START anywhere from index 0 to 'i'. There are exactly (i + 1) valid starting positions.
- A valid substring containing this character can END anywhere from index 'i' to 'N - 1'. There are exactly (N - i) valid ending positions.
Therefore, the exact number of substrings that will contain the character at index 'i' is (i + 1) * (N - i).
We simply iterate through the string, and whenever we hit a vowel, we add its mathematical contribution to our total sum.

VISUALIZATION (word = "aba"):
Length N = 3.

Index 0: 'a' (Vowel)
- Starts: (0 + 1) = 1
- Ends: (3 - 0) = 3
- Contribution: 1 * 3 = 3 substrings ("a", "ab", "aba"). Add 3.

Index 1: 'b' (Not a vowel). Skip.

Index 2: 'a' (Vowel)
- Starts: (2 + 1) = 3
- Ends: (3 - 2) = 1
- Contribution: 3 * 1 = 3 substrings ("aba", "ba", "a"). Add 3.

Total = 3 + 3 = 6 ✓
"""

# STEP 1: Initialize an accumulator for the total vowels.
# STEP 2: Iterate through the string, capturing both the index and the character.
# STEP 3: If the character is a vowel, calculate its substring contribution using the combinatorics formula.
# STEP 4: Add the contribution to the accumulator and return it after the loop.

class Solution:
    def countVowels(self, word: str) -> int:
        
        n = len(word)
        total_vowels = 0
        
        # Traverse the string in O(N) time
        for i, char in enumerate(word):
            
            # Check if the character is a vowel using a fast string lookup
            if char in "aeiou":
                
                # Formula: (choices for starting index) * (choices for ending index)
                # Adds exactly how many substrings will encapsulate this specific vowel
                total_vowels += (i + 1) * (n - i)
                
        return total_vowels

"""
WHY EACH PART:
- char in "aeiou": Python resolves inclusion checks in small constant strings/sets in O(1) time. Highly efficient.
- (i + 1) * (n - i): The combinatorial rule of product. It completely eliminates the need for nested loops or physical substring generation.

KEY TECHNIQUE:
- Contribution Technique: Flipping the iteration target. Instead of "what items are inside this container", ask "how many containers hold this specific item".
- Mathematical Combinatorics: Replacing simulation with algebraic deduction.

EDGE CASES:
- No vowels in the string (e.g., "xyz"): The condition `if char in "aeiou"` is never met, safely returning 0.
- All vowels (e.g., "aeiou"): Each vowel calculates its geometric weight and adds up perfectly without overlapping logic issues.

TIME COMPLEXITY: O(N) - We iterate through the string of length N exactly once. The math calculations inside are strictly O(1).
SPACE COMPLEXITY: O(1) - No extra data structures or substrings are allocated in memory. We only use two integer variables.
"""

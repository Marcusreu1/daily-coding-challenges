# 1641. Count Sorted Vowel Strings
# Difficulty: Medium
# https://leetcode.com/problems/count-sorted-vowel-strings/

"""
PROBLEM:
Given an integer n, return the number of strings of length n that consist only of vowels (a, e, i, o, u) and are lexicographically sorted.

EXAMPLES:
Input: n = 1 → Output: 5
Explanation: The 5 sorted strings that consist of vowels only are ["a","e","i","o","u"].

Input: n = 2 → Output: 15
Explanation: The 15 sorted strings are ["aa","ae","ai","ao","au","ee","ei","eo","eu","ii","io","iu","oo","ou","uu"].
Note that "ea" is not a valid string since 'e' comes after 'a' in the alphabet.

CONSTRAINTS:
- 1 <= n <= 50

MATH RULES (COMBINATORICS):
This problem can be mapped to the "Stars and Bars" combinatorics theorem.
We need to choose 'n' items from 5 distinct options (a, e, i, o, u) with replacement.
Because the result must be sorted, any combination of chosen vowels has exactly ONE valid permutation.
Formula: C(n + k - 1, k - 1) where k = 5 vowels.
C(n + 5 - 1, 5 - 1) = C(n + 4, 4)

Expanded Formula:
Result = (n + 4) * (n + 3) * (n + 2) * (n + 1) / 24

VISUALIZATION (n=2):
We need 2 characters (stars: **) and we have 5 vowels (requiring 4 bars: | | | | to separate them).
Total slots = n + 4 = 6
We need to choose 4 slots for the bars.

Example 1: * | * | | |  -> 1 'a', 1 'e', 0 'i', 0 'o', 0 'u' -> "ae"
Example 2: * * | | | |  -> 2 'a', 0 'e', 0 'i', 0 'o', 0 'u' -> "aa"
Example 3: | | | | * *  -> 0 'a', 0 'e', 0 'i', 0 'o', 2 'u' -> "uu"

Total valid strings = C(6, 4) = (6 * 5 * 4 * 3) / 24 = 15 ✓
"""

# STEP 1: Use the combinations with repetition formula.
# STEP 2: Multiply (n+4), (n+3), (n+2), and (n+1).
# STEP 3: Use integer division by 24 (which is 4 factorial).
# STEP 4: Return the computed integer.

class Solution:
    def countVowelStrings(self, n: int) -> int:
        
        # Apply the simplified combinatorics formula C(n+4, 4)
        result = (n + 4) * (n + 3) * (n + 2) * (n + 1) // 24
        
        return result

"""
WHY EACH PART:
- (n + 4): The first term of the descending factorial for C(n+4, 4)
- // 24: Integer division by 4! (4 * 3 * 2 * 1 = 24) to complete the combination formula
- integer division (//) instead of normal division (/): Ensures the function returns an integer type as required, avoiding float conversion errors.

HOW IT WORKS (Example: n = 2):

Initial: n = 2

Execution:
├── n + 4 = 6
├── n + 3 = 5
├── n + 2 = 4
├── n + 1 = 3
├── total_multiplication = 6 * 5 * 4 * 3 = 360
├── result = 360 // 24
└── result = 15

Return 15 ✓

KEY TECHNIQUE:
- Combinatorics Math: Translating a string generation/counting problem into a pure mathematical formula to bypass iteration completely.
- O(1) Computation: Replacing dynamic programming (which would take O(n) time) with a constant-time equation.

EDGE CASES:
- n = 1: (5 * 4 * 3 * 2) // 24 = 120 // 24 = 5 ✓
- Max n (50): Evaluates instantly without recursive depth limits or memory issues.

TIME COMPLEXITY: O(1) - The mathematical operations take constant time regardless of the size of n.
SPACE COMPLEXITY: O(1) - No auxiliary data structures are used, only integer variables.

CONCEPTS USED:
- Combinatorics (Stars and bars theorem)
- Permutations and Combinations
- Integer division in Python
"""

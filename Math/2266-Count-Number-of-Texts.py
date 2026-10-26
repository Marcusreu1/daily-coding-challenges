# 2266. Count Number of Texts
# Difficulty: Medium
# https://leetcode.com/problems/count-number-of-texts/

"""
PROBLEM:
Alice is texting Bob using a classic T9 phone keypad.
- '2' maps to "a", "b", "c".
- '3' maps to "d", "e", "f".
- ...
- '7' maps to "p", "q", "r", "s".
- '9' maps to "w", "x", "y", "z".
Given a string pressedKeys representing the keys Alice pressed, return the total number of possible text messages she could have meant.
Since the answer may be very large, return it modulo 10^9 + 7.

EXAMPLES:
Input: pressedKeys = "22233" → Output: 8
Explanation: 
The valid decodings for "222" are: "a" + "a" + "a", "a" + "b", "b" + "a", and "c". (4 ways)
The valid decodings for "33" are: "d" + "d" and "e". (2 ways)
Total ways by the rule of product = 4 * 2 = 8.

Input: pressedKeys = "222222222222222222222222222222222222" → Output: 82876089
Explanation: Due to combinatorial explosion, the number is huge. Modulo 10^9 + 7 is applied.

CONSTRAINTS:
- 1 <= pressedKeys.length <= 10^5
- pressedKeys only consists of digits from '2' to '9'.

MATH RULES (1D DYNAMIC PROGRAMMING & MODULAR ARITHMETIC):
This is a bounded variation of the "Climbing Stairs" / Fibonacci sequence problem.
To decode the string up to index 'i', we can look back:
1 step: If we take 1 character (always valid).
2 steps: If the last 2 characters are identical.
3 steps: If the last 3 characters are identical.
4 steps: If the last 4 characters are identical AND the character is '7' or '9'.
Therefore, dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] (conditionally).
By maintaining a rolling DP array and applying modulo 10^9 + 7 at each addition step, we bypass recursive exponential time and integer memory overflows entirely.
"""

# STEP 1: Initialize the DP array of size N+1 to store the valid combinations up to each prefix length.
# STEP 2: Base case: dp[0] = 1 (1 way to decode an empty prefix).
# STEP 3: Iterate through the string. By default, pull the combinations from dp[i-1].
# STEP 4: If constraints are met (matching consecutive characters), pull combinations from dp[i-2], dp[i-3], and conditionally dp[i-4].
# STEP 5: Apply modulo 10^9 + 7 iteratively and return the final dp state.

class Solution:
    def countTexts(self, pressedKeys: str) -> int:
        MOD = 10**9 + 7
        n = len(pressedKeys)
        
        # dp[i] represents the number of valid messages for the first 'i' characters
        dp = [0] * (n + 1)
        dp[0] = 1 
        
        for i in range(1, n + 1):
            
            # Base case: Group of 1 (a single key press)
            dp[i] = dp[i - 1]
            
            # Group of 2: Must be identical to the previous character
            if i >= 2 and pressedKeys[i - 1] == pressedKeys[i - 2]:
                dp[i] = (dp[i] + dp[i - 2]) % MOD
                
                # Group of 3: Must be identical to the previous 2 characters
                if i >= 3 and pressedKeys[i - 1] == pressedKeys[i - 3]:
                    dp[i] = (dp[i] + dp[i - 3]) % MOD
                    
                    # Group of 4: Must be identical to the previous 3 characters AND specifically be '7' or '9'
                    if i >= 4 and pressedKeys[i - 1] in '79' and pressedKeys[i - 1] == pressedKeys[i - 4]:
                        dp[i] = (dp[i] + dp[i - 4]) % MOD
                        
        return dp[n]

"""
WHY EACH PART:
- MOD = 10**9 + 7: Standard cryptographic prime used in competitive programming to prevent integer overflow and bounds-check crashes in strictly typed languages.
- dp[0] = 1: The mathematical identity foundation. If we match a 3-character group at the very start of the string (i=3), we look back to dp[0]. Adding dp[0] (which is 1) successfully registers that 1 valid combination.
- Nested if statements: Optimization. If the 2nd character doesn't match, it is mathematically impossible for the 3rd or 4th to form a valid contiguous block, so we short-circuit and skip checking them.

KEY TECHNIQUE:
- Dynamic Programming (Prefix Accumulation): Breaking a massive combinatorial tree into overlapping subproblems stored linearly.
- State Lookback: Reusing previous computed states instead of recalculating permutations.

EDGE CASES:
- String of unique characters (e.g., "2345"): None of the `if` conditions trigger. dp[i] purely copies dp[i-1]. Final result is 1 way. Correct.
- String with all '9's: Triggers the Tetranacci-like sequence (adding up to 4 previous states), correctly reflecting the 4-letter capacity of the '9' key.

TIME COMPLEXITY: O(N) - We iterate through the string of length N exactly once. Inside the loop, we perform at most 4 O(1) character checks and additions. Total time is strictly linear.
SPACE COMPLEXITY: O(N) - We allocate an array of size N + 1. Since N is at most 10^5, this takes negligible memory (~400KB in Python). (This can theoretically be optimized to O(1) by only keeping the last 4 variables, but O(N) is safer and vastly more readable).
"""

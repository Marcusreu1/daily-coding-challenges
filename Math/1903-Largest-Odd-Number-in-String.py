# 1903. Largest Odd Number in String
# Difficulty: Easy
# https://leetcode.com/problems/largest-odd-number-in-string/

"""
PROBLEM:
You are given a string num, representing a large integer. Return the largest-valued odd integer (as a string) that is a non-empty substring of num, or an empty string "" if no odd integer exists.
A substring is a contiguous sequence of characters within a string.

EXAMPLES:
Input: num = "52" → Output: "5"
Explanation: The only non-empty substrings are "5", "2", and "52". "5" is the only odd number.

Input: num = "4206" → Output: ""
Explanation: There are no odd numbers in "4206".

Input: num = "35427" → Output: "35427"
Explanation: "35427" is already an odd number.

CONSTRAINTS:
- 1 <= num.length <= 10^5
- num only consists of digits and does not contain any leading zeros.

MATH RULES (NUMBER PARITY & GREEDY STRATEGY):
A number's parity (whether it is odd or even) is determined SOLELY by its very last digit. 
If a number ends in 1, 3, 5, 7, or 9, the entire number is odd, regardless of the digits preceding it.
To maximize the value of the substring, we want it to be as long as possible and start from the most significant digit (the extreme left).
Therefore, the optimal (greedy) strategy is to scan the string from right to left. The moment we find an odd digit, we return the entire prefix of the string up to and including that digit.

VISUALIZATION (num = "35426"):
Scan from right to left:
Index 4: '6' -> Even.
Index 3: '2' -> Even.
Index 2: '4' -> Even.
Index 1: '5' -> ODD!

Stop searching. The largest odd number must end here.
Take everything from the start up to Index 1.
Result: "35" ✓
"""

# STEP 1: Loop through the string in reverse (from the last character down to the first).
# STEP 2: Check if the current digit is odd.
# STEP 3: If an odd digit is found, return the substring from the beginning of 'num' up to this digit's index (inclusive).
# STEP 4: If the loop finishes without finding any odd digit, return an empty string.

class Solution:
    def largestOddNumber(self, num: str) -> str:
        
        # Traverse the string backwards
        for i in range(len(num) - 1, -1, -1):
            
            # Check if the current character is an odd digit
            # A fast string inclusion check avoids the overhead of casting to an integer
            if num[i] in {"1", "3", "5", "7", "9"}:
                
                # Return the prefix string up to the current odd digit
                return num[:i + 1]
                
        # If no odd digits exist in the entire string
        return ""

"""
WHY EACH PART:
- range(len(num) - 1, -1, -1): The perfect setup for a right-to-left scan. Starts at the last index and stops at 0.
- in {"1", "3", "5", "7", "9"}: A set lookup in Python is O(1). This is significantly faster and more memory-efficient than converting the character to an integer (int(num[i]) % 2 != 0).
- num[:i + 1]: Python's slicing syntax. It grabs everything from index 0 up to, but not including, i + 1. This ensures the odd digit at index i is included.

KEY TECHNIQUE:
- Greedy Algorithm: Finding the global maximum by making the immediate local optimal choice (the rightmost odd digit ensures the longest possible valid prefix).
- String Slicing over Type Casting: Treating massive numbers as strings prevents the program from crashing due to memory overflow when integers exceed standard 64-bit limits.

EDGE CASES:
- The entire string is odd (e.g., "35427"): The very first check at the last index succeeds, immediately returning the full string in O(1) time.
- The string contains no odd digits (e.g., "2468"): The loop scans every character, fails gracefully, and returns "" without errors.

TIME COMPLEXITY: O(N) - In the worst-case scenario (all even digits), we iterate through every character of the string of length N exactly once.
SPACE COMPLEXITY: O(1) - We only evaluate characters in place. (Note: Returning the sliced string allocates O(N) space for the output, but auxiliary working space remains O(1)).

CONCEPTS USED:
- Greedy Strategy
- Array/String Reverse Traversal
- Parity Math Logic
- Hash Set Lookup
"""

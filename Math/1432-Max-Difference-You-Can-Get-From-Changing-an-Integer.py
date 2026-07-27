# 1432. Max Difference You Can Get From Changing an Integer
# Difficulty: Medium
# https://leetcode.com/problems/max-difference-you-can-get-from-changing-an-integer/

"""
PROBLEM:
You are given an integer `num`. You will apply the following steps exactly two times to create two new integers `a` and `b`:
- Pick a digit x (0 <= x <= 9).
- Pick another digit y (0 <= y <= 9). The digit y can be equal to x.
- Replace all the occurrences of x in the decimal representation of `num` by y.
- The new integer cannot have any leading zeros, also the new integer cannot be 0.
Let `a` and `b` be the results of applying the operations to `num` the first and second times, respectively.
Return the max difference a - b.

EXAMPLES:
Input: num = 555
Output: 888
(Explanation: 
First time: pick x = 5 and y = 9. a = 999.
Second time: pick x = 5 and y = 1. b = 111.
Difference = 999 - 111 = 888)

Input: num = 9
Output: 8
(Explanation: a = 9, b = 1. Difference = 8)

Input: num = 123456
Output: 820000
(Explanation: 
a: replace 1 with 9 -> 923456
b: replace 2 with 0 -> 103456
Difference = 923456 - 103456 = 820000)

CONSTRAINTS:
- 1 <= num <= 10^8

ALGORITHM LOGIC (Positional Greedy & String Manipulation):
1. To maximize `a - b`, we must make `a` as large as possible and `b` as small as possible.
2. We treat the numbers as strings to easily access positional digits and use global replacement methods.
3. Maximize `a`: Scan from left to right. Find the first digit that is NOT '9'. Replace all its occurrences with '9'. If all are '9', `a` remains the same.
4. Minimize `b`: 
   - Rule 1: The number cannot have leading zeros.
   - If the first digit is NOT '1', the best we can do is replace all its occurrences with '1'.
   - If the first digit IS '1', we leave it alone (replacing it with 0 invalidates the number). 
   - Instead, we scan from the second digit onwards to find the first digit that is neither '0' nor '1', and replace all its occurrences with '0'.
5. Convert the generated strings back to integers and return their difference.

VISUALIZATION (num = 10023):
s = "10023"

Maximize (a):
Index 0: '1' != '9' -> Replace '1' with '9'.
a = "90023". (Loop breaks)

Minimize (b):
Index 0 is '1'. So we scan from Index 1 onwards.
Index 1: '0'. (Ignore, already 0)
Index 2: '0'. (Ignore, already 0)
Index 3: '2'. It's not '0' and not '1'! -> Replace '2' with '0'.
b = "10003". (Loop breaks)

Difference: 90023 - 10003 = 80020. ✓
"""

# STEP 1: Cast the integer to a string to enable character indexing and replacement
# STEP 2: Execute the Greedy logic to maximize the number `a`
# STEP 3: Execute the contextual Greedy logic to minimize the number `b` considering the leading zero constraint
# STEP 4: Cast the results back to integers and subtract them

class Solution:
    def maxDiff(self, num: int) -> int:
        
        s = str(num)
        max_num = s
        min_num = s
        
        # Phase 1: Maximize the number
        for char in s:
            if char != '9':
                max_num = s.replace(char, '9')                       # Replace globally and immediately stop
                break
                
        # Phase 2: Minimize the number
        if s[0] != '1':
            # If it doesn't start with 1, turn the first digit into 1
            min_num = s.replace(s[0], '1')
        else:
            # If it starts with 1, find the next available inner digit to turn into 0
            for char in s[1:]:
                if char != '0' and char != '1':
                    min_num = s.replace(char, '0')
                    break
                    
        return int(max_num) - int(min_num)

"""
WHY EACH PART:
- s.replace(char, 'new_char'): Python's string `.replace()` replaces all instances of the character. This perfectly matches the problem constraint "Replace all the occurrences of x".
- if char != '0' and char != '1': When minimizing an inner digit, we ignore '0' because it's already optimal. We ignore '1' because if we replaced all '1's with '0', we would accidentally turn the leading '1' into a '0', violating the leading-zero rule.
- int(max_num) - int(min_num): Safely converts the processed strings back to math objects to execute the final subtraction.

HOW IT WORKS (Example: num = 111):
Maximize: First non-9 is '1'. Replace all '1's with '9'. max_num = "999".
Minimize: First char is '1'. Scans remaining "11". All chars are '1' (ignored). Loop finishes naturally without replacing. min_num = "111".
Result: 999 - 111 = 888. ✓

KEY TECHNIQUE:
- Greedy Algorithm (Positional optimization)
- String Manipulation and Global Replacement

EDGE CASES:
- num is a single digit (e.g., 9): Handled perfectly. 9 becomes 9 for max, 9 becomes 1 for min. 9 - 1 = 8. ✓
- Numbers composed entirely of 1s or 9s (e.g., 9999): The loops complete without triggering replacements, returning the identity values properly. ✓

TIME COMPLEXITY: O(L) - Where L is the number of digits in `num`. Since `num` <= 10^8, L is at most 8. Scanning a string of length 8 and replacing characters executes in extremely small, effectively O(1) constant time.
SPACE COMPLEXITY: O(L) - We store the string representation of the number and its modified versions. For a max 8-character string, this takes O(1) space.
"""

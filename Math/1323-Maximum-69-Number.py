# 1323. Maximum 69 Number
# Difficulty: Easy
# https://leetcode.com/problems/maximum-69-number/

"""
PROBLEM:
You are given a positive integer `num` consisting only of digits 6 and 9.
Return the maximum number you can get by changing at most one digit (6 becomes 9, and 9 becomes 6).

EXAMPLES:
Input: num = 9669
Output: 9969
(Explanation: 
Changing the first digit results in 6669.
Changing the second digit results in 9969.
Changing the third digit results in 9699.
Changing the fourth digit results in 9666.
The maximum number is 9969.)

Input: num = 9996
Output: 9999
(Explanation: Changing the last digit 6 to 9 results in the maximum number.)

Input: num = 9999
Output: 9999
(Explanation: It is better not to apply any change.)

CONSTRAINTS:
- 1 <= num <= 10^4
- num consists of only 6 and 9 digits.

ALGORITHM LOGIC (Greedy Approach via String Manipulation):
1. To maximize a number, we should always aim to increase its most significant digit (the leftmost digit).
2. Since our only options are 6 and 9, the only way to increase the number's value is by turning a 6 into a 9.
3. Turning a 9 into a 6 would strictly decrease the number's value, which goes against our goal.
4. Therefore, the optimal strategy is to find the very first '6' (from left to right) and change it to a '9'.
5. If there are no '6's in the number, we make 0 changes.
6. Python's string `replace()` method takes an optional third argument that limits the number of replacements, making it the perfect tool for this greedy strategy.

VISUALIZATION (num = 9669):
Initial Integer: 9669

Step 1 (Cast to String): 
"9669"

Step 2 (Replace '6' with '9', max 1 time):
Search index 0: '9' (Skip)
Search index 1: '6' -> Found! Replace with '9'.
Limit reached. Stop searching.
String becomes: "9969"

Step 3 (Cast back to Integer):
9969 ✓
"""

# STEP 1: Cast the integer `num` to a string representation
# STEP 2: Use the `.replace()` method to swap the character '6' for '9'
# STEP 3: Pass `1` as the third argument to ensure ONLY the first occurrence is replaced
# STEP 4: Cast the modified string back to an integer
# STEP 5: Return the integer

class Solution:
    def maximum69Number (self, num: int) -> int:
        
        # We chain type casting and string replacement into a single highly-optimized line
        return int(str(num).replace('6', '9', 1))

"""
WHY EACH PART:
- str(num): We convert to a string to gain access to sequential character manipulation without needing modulo/division math loops.
- .replace('6', '9', 1): The greedy engine. By setting the `count` parameter to 1, Python scans from left to right and terminates the replacement operation the exact moment the first '6' is swapped.
- int(...): Re-casting to satisfy the function's strict return type hint (`-> int`).

HOW IT WORKS (Example: num = 9999):
str(num) -> "9999"
.replace('6', '9', 1) -> Tries to find '6'. Fails to find any. Returns original string "9999".
int("9999") -> 9999
Returns 9999. ✓

KEY TECHNIQUE:
- Greedy Strategy: Taking the immediately optimal move at the earliest opportunity (leftmost position) without needing to evaluate the rest of the sequence.
- Limited String Replacement: Using built-in string methods in Python instead of mathematical digit extraction for clearer, faster code when dealing with positional numeral logic.

EDGE CASES:
- Number contains no 6s (e.g., 9999): Handled gracefully, `.replace` does nothing, returns 9999. ✓
- Number starts with 6 (e.g., 6999): The first digit is changed immediately, returns 9999. ✓
- Smallest possible constraint (e.g., num = 6): Converts to '9', returns 9. ✓

TIME COMPLEXITY: O(L) - Where L is the number of digits in `num`. Converting to string, scanning for '6', and converting back to integer all take time proportional to the length of the number. Since the max constraint is 10^4 (only 4 digits), this executes in effectively O(1) constant time.
SPACE COMPLEXITY: O(L) - We allocate a tiny amount of memory to hold the string representation of the 4-digit number. Effectively O(1).

CONCEPTS USED:
- Greedy Algorithms
- Type Casting
- String Manipulation
"""

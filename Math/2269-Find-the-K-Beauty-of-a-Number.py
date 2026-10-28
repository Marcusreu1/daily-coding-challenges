# 2269. Find the K-Beauty of a Number
# Difficulty: Easy
# https://leetcode.com/problems/find-the-k-beauty-of-a-number/

"""
PROBLEM:
The k-beauty of an integer num is defined as the number of substrings of num when it is read as a string that meet the following conditions:
- It has a length of k.
- It is a divisor of num.
Given integers num and k, return the k-beauty of num.
Note:
- Leading zeros are allowed.
- 0 is not a divisor of any value.
- A substring is a contiguous sequence of characters in a string.

EXAMPLES:
Input: num = 24042, k = 2 → Output: 2
Explanation: The following are the substrings of num of length k:
- "24" from "24042": 24 is a divisor of 24042.
- "40" from "24042": 40 is not a divisor of 24042.
- "04" from "24042": 4 is not a divisor of 24042.
- "42" from "24042": 42 is not a divisor of 24042.
The k-beauty is 2.

Input: num = 430043, k = 2 → Output: 2
Explanation: The following are the substrings of num of length k:
- "43" from "430043": 43 is a divisor of 430043.
- "30" from "430043": 30 is not a divisor of 430043.
- "00" from "430043": 0 is not a divisor of 430043.
- "04" from "430043": 4 is not a divisor of 430043.
- "43" from "430043": 43 is a divisor of 430043.
The k-beauty is 2.

CONSTRAINTS:
- 1 <= num <= 10^9
- 1 <= k <= num.length (taking num as a string)

MATH RULES (SLIDING WINDOW & SHORT-CIRCUIT EVALUATION):
To extract all contiguous sub-segments of length 'k', we apply a Sliding Window over the string representation of the number.
The window starts at index 0 and slides to index (N - k), yielding exactly (N - k + 1) substrings.
A mathematical trap in this problem is dealing with substrings composed entirely of zeros (e.g., "00"). 
Division by zero is undefined in mathematics and causes a ZeroDivisionError in hardware/compilers.
To prevent crashes optimally, we use Short-Circuit logical evaluation: `divisor != 0 and num % divisor == 0`.
If the first condition evaluates to False, the CPU instantly skips the second condition, averting the fatal modulo operation.
"""

# STEP 1: Convert the integer into a string to enable positional slicing.
# STEP 2: Iterate using a sliding window of fixed length 'k'.
# STEP 3: Cast the captured substring back to an integer. Python handles leading zeros automatically.
# STEP 4: Perform a short-circuited check to ensure the divisor is non-zero, then check if it perfectly divides num.
# STEP 5: Increment the k_beauty counter for valid occurrences and return it.

class Solution:
    def divisorSubstrings(self, num: int, k: int) -> int:
        
        # Convert integer to string to enable slicing
        num_str = str(num)
        k_beauty = 0
        
        # Slide a window of size 'k' across the string
        for i in range(len(num_str) - k + 1):
            
            # Extract the substring and cast it to integer (removes leading zeros natively)
            current_divisor = int(num_str[i : i + k])
            
            # Short-circuit evaluation protects against ZeroDivisionError
            if current_divisor != 0 and num % current_divisor == 0:
                k_beauty += 1
                
        return k_beauty

"""
WHY EACH PART:
- range(len(num_str) - k + 1): Computes the exact number of valid window placements without going out of bounds.
- int(num_str[i : i + k]): The slice grabs the raw characters. `int()` instantly resolves mathematical conversions like "04" -> 4 or "00" -> 0.
- current_divisor != 0 and num % current_divisor == 0: The order is critical. The non-zero validation MUST precede the modulo operation to act as a mathematical shield.

KEY TECHNIQUE:
- Fixed Sliding Window: An O(N) iterative pattern used universally to traverse contiguous subsections of arrays/strings.
- Guard Clauses (Short-Circuit): Leveraging language architecture to prevent algorithmic crashes with minimal code.

EDGE CASES:
- Multiple zeros in the string (e.g., num=100000, k=2): Substrings "00" evaluate to 0. Protected flawlessly by the guard clause.
- Substring evaluates to the entire number (e.g., k = length of num): Loop runs exactly 1 time. num % num == 0. Returns 1. Correct.

TIME COMPLEXITY: O(N) - Where N is the number of digits in `num`. Since `num <= 10^9`, N is at most 10. The loop runs at most 10 times, making it O(1) in practical computational terms.
SPACE COMPLEXITY: O(N) - We allocate memory for the string representation of the number, which takes a negligible constant space of up to 10 characters.
"""

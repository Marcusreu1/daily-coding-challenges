# 1295. Find Numbers with Even Number of Digits
# Difficulty: Easy
# https://leetcode.com/problems/find-numbers-with-even-number-of-digits/

"""
PROBLEM:
We are given an integer array called `nums`. Our objective is to count how many of these 
integers possess an even number of digits and return that total count.

EXAMPLES:
Input: nums = [12, 345, 2, 6, 7896]
Output: 2
(Explanation: 
- 12 has 2 digits (which is even).
- 345 has 3 digits (which is odd).
- 2 and 6 have 1 digit each (odd).
- 7896 has 4 digits (which is even).
Therefore, only 12 and 7896 meet the condition, giving us a total of 2.)

Input: nums = [555, 901, 482, 1771]
Output: 1
(Explanation: Only 1771 has an even amount of digits - exactly 4).

CONSTRAINTS:
- 1 <= nums.length <= 500
- 1 <= nums[i] <= 10^5

ALGORITHM LOGIC (String Conversion Strategy):
1. While it is possible to count digits mathematically (using log10 or repeated division by 10), 
   Python's built-in string conversion is heavily optimized in C and highly readable.
2. We can convert any integer into a string using str().
3. Once it is a string, we can measure its length (number of digits) using len().
4. We then use the modulo operator (% 2 == 0) to check if that length is an even number.
5. We iterate through the array, incrementing a counter every time this condition is met.
"""

# STEP 1: Initialize a counter for the numbers that meet our criteria
# STEP 2: Iterate through every number in the input array
# STEP 3: Convert the number to a string and measure its length
# STEP 4: If the length is perfectly divisible by 2 (even), increment the counter
# STEP 5: Return the final counter

class Solution:
    def findNumbers(self, nums: list[int]) -> int:
        
        even_count = 0                                               # Counter for valid numbers
        
        for num in nums:                                             # Traverse the array
            
            if len(str(num)) % 2 == 0:                               # Stringify, count length, check parity
                even_count += 1                                      # Increment if even digits
                
        return even_count                                            # Return the final count

"""
WHY EACH PART:
- even_count = 0: We need an independent additive accumulator to keep track of our findings.
- str(num): Translates the mathematical integer into an iterable sequence of characters.
- len(...): Counts the characters. Since there are no negative numbers in the constraints (which would add a '-' character), this perfectly represents the digit count.
- % 2 == 0: The universal programming standard to check if any integer is even.

HOW IT WORKS (Example: nums = [12, 345]):
Iteration 1:
num = 12
str(12) = "12"
len("12") = 2
2 % 2 == 0 ? Yes. even_count becomes 1.

Iteration 2:
num = 345
str(345) = "345"
len("345") = 3
3 % 2 == 0 ? No. even_count remains 1.

Loop ends. Returns 1. ✓

KEY TECHNIQUE:
- Type Casting (Integer to String): Leveraging Python's strong internal string manipulation for tasks that would otherwise require math loops.

EDGE CASES:
- Array with one element (e.g., [10]): Evaluates correctly. ✓
- Numbers up to 10^5 (e.g., 100000): Evaluates to 6 digits, returns correctly. ✓

TIME COMPLEXITY: O(N) - Where N is the number of elements in the array. Converting to string and checking length takes time proportional to the number of digits, but since the max number is 10^5 (6 digits), this operation is effectively O(1) per number. Total time scales linearly with N.
SPACE COMPLEXITY: O(1) - We only create short-lived string representations in memory and a single counter variable. No scaling extra space is used.

CONCEPTS USED:
- Array Iteration
- Type Casting
- String Length 
- Modulo Arithmetic
"""

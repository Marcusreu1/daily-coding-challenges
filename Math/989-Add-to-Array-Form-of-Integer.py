# 989. Add to Array-Form of Integer
# Difficulty: Easy
# https://leetcode.com/problems/add-to-array-form-of-integer/

"""
PROBLEM:
The array-form of an integer num is an array representing its digits in left to right order.
For example, for num = 1321, the array form is [1,3,2,1].
Given num, the array-form of an integer, and an integer k, return the array-form of the integer num + k.

EXAMPLES:
Input: num = [1,2,0,0], k = 34
Output: [1,2,3,4] (1200 + 34 = 1234)

Input: num = [2,7,4], k = 181
Output: [4,5,5] (274 + 181 = 455)

Input: num = [2,1,5], k = 806
Output: [1,0,2,1] (215 + 806 = 1021)

CONSTRAINTS:
- 1 <= num.length <= 10^4
- 0 <= num[i] <= 9
- num does not contain any leading zeros except for the zero itself.
- 1 <= k <= 10^4

MATHEMATICAL REDUCTION:
Instead of converting the large array into a massive integer (which can cause overflow in strictly typed languages), we simulate grade-school addition from right to left.
The clever optimization here is treating the entire integer `k` as the "carry".
For the rightmost digit, we add the entire value of `k` to it. 
The new digit to write down is `(num[i] + k) % 10`.
The new carry to pass to the next column is `(num[i] + k) // 10`.
We repeat this moving leftwards until both the array is exhausted and `k` becomes 0.

VISUALIZATION (num = [2,1,5], k = 806):
We iterate from right to left.

Position 2 (Value = 5):
total = 5 + 806 = 811
write = 811 % 10 = 1
k (carry) = 811 // 10 = 81

Position 1 (Value = 1):
total = 1 + 81 = 82
write = 82 % 10 = 2
k (carry) = 82 // 10 = 8

Position 0 (Value = 2):
total = 2 + 8 = 10
write = 10 % 10 = 0
k (carry) = 10 // 10 = 1

Array exhausted, but k > 0.
total = 1
write = 1 % 10 = 1
k (carry) = 1 // 10 = 0

Result built backwards: [1, 2, 0, 1]
Reversed result: [1, 0, 2, 1] ✓
"""

# STEP 1: Initialize an empty result array and a pointer at the end of `num`.
# STEP 2: Loop backwards while there are still digits in `num` OR `k` is greater than 0.
# STEP 3: Add the current array digit to `k` (k acts as our running total/carry).
# STEP 4: Append the last digit of the new `k` to the result array.
# STEP 5: Truncate the last digit from `k` to act as the carry for the next iteration.
# STEP 6: Reverse the result array since it was built from least significant digit to most.

class Solution:
    def addToArrayForm(self, num: list[int], k: int) -> list[int]:
        
        result = []                                                            # Build result here
        i = len(num) - 1                                                       # Pointer to the end of num
        
        while i >= 0 or k > 0:                                                 # While work remains
            
            if i >= 0:                                                         # If we are still inside the array bounds
                k += num[i]                                                    # Add the current digit directly to k
                i -= 1                                                         # Move pointer left
                
            result.append(k % 10)                                              # Extract the rightmost digit and append
            k = k // 10                                                        # The rest of the number becomes the carry
            
        return result[::-1]                                                    # Reverse the built array to restore order

"""
WHY EACH PART:
- while i >= 0 or k > 0: Ensures we don't stop prematurely. We must continue if there are still digits in the array, OR if `num` is exhausted but we still have a leftover carry from `k` (e.g., [9,9] + 1).
- k += num[i]: Instead of creating a separate `carry` variable, we smartly reuse `k`.
- k % 10: Extracts the least significant digit (0-9) to store in our current position.
- k // 10: Integer division chops off the least significant digit, passing the rest as the carry for the next power of 10.
- result[::-1]: Appending to a list is an O(1) operation. Inserting at index 0 (result.insert(0, val)) is an O(N) operation. Therefore, appending and reversing at the very end is significantly more efficient.

HOW IT WORKS (Example: [2,7,4], k = 181):

Initial: i = 2, k = 181, result = []

Iteration 1 (i = 2):
├── k = 181 + num[2] = 181 + 4 = 185
├── result.append(185 % 10) -> result = [5]
└── k = 185 // 10 = 18

Iteration 2 (i = 1):
├── k = 18 + num[1] = 18 + 7 = 25
├── result.append(25 % 10) -> result = [5, 5]
└── k = 25 // 10 = 2

Iteration 3 (i = 0):
├── k = 2 + num[0] = 2 + 2 = 4
├── result.append(4 % 10) -> result = [5, 5, 4]
└── k = 4 // 10 = 0

Exit loop: (i < 0 and k == 0).

result[::-1] = [4, 5, 5]
return [4, 5, 5] ✓

KEY TECHNIQUE:
- Two-pointer / Right-to-Left Traversal.
- Reusing the addend (`k`) as a mega-carry to simplify state tracking.
- Build and reverse string/array generation pattern.

EDGE CASES:
- Carry expands the array length ([9,9,9,9] + 1): Handled gracefully because the loop continues as long as `k > 0`, pushing the final '1' correctly to yield [1,0,0,0,0]. ✓
- `k` is longer than `num` ([0] + 1000): Handled perfectly. Array index runs out, but `k` continuously unloads its digits into the result array. ✓
- Zero addition ([0] + 0): Result handles correctly returning [0]. ✓

TIME COMPLEXITY: O(max(N, log10(K))) - We iterate up to the length of the array N, or the number of digits in K, whichever is strictly larger.
SPACE COMPLEXITY: O(max(N, log10(K))) - To hold the resulting array which will be at most 1 element larger than the max between N and the length of K.

CONCEPTS USED:
- Arrays
- Mathematical Simulation
"""

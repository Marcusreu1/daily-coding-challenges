# 1802. Maximum Value at a Given Index in a Bounded Array
# Difficulty: Medium
# https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/

"""
PROBLEM:
You are given three positive integers: n, index, and maxSum. You want to construct an array nums (0-indexed) that satisfies the following conditions:
- nums.length == n
- nums[i] is a positive integer where 1 <= nums[i].
- abs(nums[i] - nums[i+1]) <= 1 where 0 <= i < n-1.
- The sum of all the elements of nums does not exceed maxSum.
- nums[index] is maximized.
Return nums[index] of the constructed array.

EXAMPLES:
Input: n = 4, index = 2,  maxSum = 6 → Output: 2
Explanation: nums = [1,2,2,1] is one array that satisfies all the conditions.
There are no arrays that satisfy all the conditions and have nums[2] == 3.

Input: n = 6, index = 1,  maxSum = 10 → Output: 3
Explanation: nums = [2,3,2,1,1,1] satisfies all the conditions.

CONSTRAINTS:
- 1 <= n <= maxSum <= 10^9
- 0 <= index < n

MATH RULES (BINARY SEARCH ON ANSWER & ARITHMETIC PROGRESSION):
To minimize the total sum while targeting a specific peak value 'x' at 'index', the adjacent values must strictly decrease by 1 until they hit 1.
Left side length = index
Right side length = n - 1 - index

For a side of length 'L' starting at value 'V' (which is x - 1):
Scenario A: The sequence hits 1 before reaching the end (V < L).
Sum = (V * (V + 1)) // 2 + (L - V) (the remaining elements are filled with 1s).
Scenario B: The sequence doesn't hit 1 (V >= L).
Sum = (L * (V + (V - L + 1))) // 2 (sum of arithmetic progression from V down to V - L + 1).

Since the required sum monotonically increases as 'x' increases, we can use Binary Search to find the maximum possible 'x'.

VISUALIZATION (n = 6, index = 1, maxSum = 10):
Let's test peak value x = 3 at index 1:
Left length = 1. Value adjacent = 2. Sum = 2. (Sequence: [2])
Right length = 4. Value adjacent = 2. Sum = (2+1) + 2 ones = 5. (Sequence: [2, 1, 1, 1])
Total Array: [2, 3, 2, 1, 1, 1]
Total Sum = 3 (peak) + 2 (left) + 5 (right) = 10.
10 <= maxSum (10), so x = 3 is valid.
"""

# STEP 1: Define a helper function to calculate the minimum sum for a given side using arithmetic progression.
# STEP 2: Initialize the binary search boundaries: left = 1, right = maxSum.
# STEP 3: Perform binary search. Set 'mid' as the candidate peak value.
# STEP 4: Calculate the total required sum using the helper function for both the left and right sides.
# STEP 5: If the sum <= maxSum, record 'mid' as a valid answer and search for a higher peak (left = mid + 1).
# STEP 6: If the sum > maxSum, the peak is too high, adjust the upper boundary (right = mid - 1).

class Solution:
    def maxValue(self, n: int, index: int, maxSum: int) -> int:
        
        def get_sum(length: int, val: int) -> int:
            if length == 0:
                return 0
                
            # If the value drops to 1 before filling the length, pad with 1s
            if val < length:
                progression_sum = (val * (val + 1)) // 2
                padding_ones = length - val
                return progression_sum + padding_ones
                
            # If the value stays > 1 throughout the length
            else:
                last_val = val - length + 1
                progression_sum = (length * (val + last_val)) // 2
                return progression_sum

        left = 1
        right = maxSum
        best_peak = 1
        
        while left <= right:
            mid = (left + right) // 2
            
            # The value adjacent to the peak is mid - 1
            left_sum = get_sum(index, mid - 1)
            right_sum = get_sum(n - 1 - index, mid - 1)
            
            total_sum = mid + left_sum + right_sum
            
            if total_sum <= maxSum:
                best_peak = mid         # Candidate is valid, save it
                left = mid + 1          # Try to find a larger peak
            else:
                right = mid - 1         # Candidate is invalid, lower the peak
                
        return best_peak

"""
WHY EACH PART:
- def get_sum(length, val): Abstracts the math logic to keep the binary search loop clean. It runs in O(1) time.
- padding_ones = length - val: Ensures the rule "positive integer (>=1)" is respected when the arithmetic sequence zeroes out.
- last_val = val - length + 1: Determines the lowest value on that side if it never hits 1.
- left = mid + 1 / right = mid - 1: Standard binary search mechanic to narrow down the search space logarithmically.

HOW IT WORKS (Example: n = 4, index = 2, maxSum = 6):

Initial: left = 1, right = 6

Iteration 1:
├── mid = 3
├── left_sum (length 2, val 2): val >= length -> 2 * (2 + 1) // 2 = 3
├── right_sum (length 1, val 2): val >= length -> 1 * (2 + 2) // 2 = 2
├── total_sum = 3 + 3 + 2 = 8
└── 8 > maxSum (6). Invalid. right = 2.

Iteration 2:
├── mid = 1
├── left_sum (length 2, val 0): val < length -> 0 + 2 ones = 2
├── right_sum (length 1, val 0): val < length -> 0 + 1 one = 1
├── total_sum = 1 + 2 + 1 = 4
└── 4 <= maxSum (6). Valid. best_peak = 1, left = 2.

Iteration 3:
├── mid = 2
├── left_sum (length 2, val 1): val < length -> 1 + 1 one = 2
├── right_sum (length 1, val 1): val >= length -> 1 * (1 + 1) // 2 = 1
├── total_sum = 2 + 2 + 1 = 5
└── 5 <= maxSum (6). Valid. best_peak = 2, left = 3.

Exit: left (3) > right (2).

return 2 ✓

KEY TECHNIQUE:
- Binary Search on Answer: Transforming an optimization problem into a decision problem (Is it possible to have peak X?) to solve it logarithmically.
- Arithmetic Series Optimization: Bypassing O(n) array simulations by using O(1) mathematical summation formulas.

EDGE CASES:
- Array of length 1 (n=1, index=0): The math logic zeroes out the left and right sums perfectly, yielding mid = maxSum.
- maxSum equals n: The array can only be filled with 1s. The binary search will gracefully converge to 1.

TIME COMPLEXITY: O(log(maxSum)) - The binary search halves the search space of size maxSum in each step. The calculations inside take O(1) time.
SPACE COMPLEXITY: O(1) - Only a few integer variables are stored.

CONCEPTS USED:
- Binary Search
- Arithmetic Progressions
- Monotonic Functions
- Boundary Logic
"""

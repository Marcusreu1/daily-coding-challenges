# 1588. Sum of All Odd Length Subarrays
# Difficulty: Easy
# https://leetcode.com/problems/sum-of-all-odd-length-subarrays/

"""
PROBLEM:
Given an array of positive integers `arr`, return the sum of all possible odd-length subarrays of `arr`.
A subarray is a contiguous subsequence of the array.

EXAMPLES:
Input: arr = [1,4,2,5,3]
Output: 58
(Explanation: The odd-length subarrays of arr and their sums are:
[1] = 1
[4] = 4
[2] = 2
[5] = 5
[3] = 3
[1,4,2] = 7
[4,2,5] = 11
[2,5,3] = 10
[1,4,2,5,3] = 15
If we add all these together we get 1 + 4 + 2 + 5 + 3 + 7 + 11 + 10 + 15 = 58)

Input: arr = [1,2]
Output: 3
(Explanation: There are only 2 subarrays of odd length, [1] and [2]. Their sum is 3.)

CONSTRAINTS:
- 1 <= arr.length <= 100
- 1 <= arr[i] <= 1000

ALGORITHM LOGIC (Mathematical Contribution Technique):
1. Generating all subarrays results in O(N^3) or O(N^2) complexity. We can achieve O(N) by calculating the independent contribution of each element to the final sum.
2. For an element at index `i`, any subarray containing this element must start at or before `i`, and end at or after `i`.
3. The number of possible starting positions is `i + 1` (from index 0 to i).
4. The number of possible ending positions is `n - i` (from index i to n-1).
5. The total number of subarrays containing `arr[i]` is strictly `(i + 1) * (n - i)`.
6. Out of all these subarrays, exactly half (rounded up) will have an odd length.
7. Therefore, the number of odd-length subarrays containing `arr[i]` is `(total_subarrays + 1) // 2`.
8. We multiply the value of the element by its odd-subarray occurrence count and accumulate it.

VISUALIZATION (arr = [1, 4, 2, 5, 3]):
For the element '2' at index i = 2:
n = 5
left_choices = 2 + 1 = 3
right_choices = 5 - 2 = 3
total_subarrays = 3 * 3 = 9.

Odd length subarrays containing '2' = (9 + 1) // 2 = 5.
(Let's manually verify: [2], [1,4,2], [4,2,5], [2,5,3], [1,4,2,5,3]. Exactly 5!).
Contribution to the total sum = 2 * 5 = 10. ✓
"""

# STEP 1: Initialize the total sum accumulator
# STEP 2: Iterate through every element linearly using its index
# STEP 3: Calculate mathematically how many total subarrays feature this element
# STEP 4: Extract the exact number of odd-length subarrays using integer floor division
# STEP 5: Multiply the array value by its occurrences and add to total sum

class Solution:
    def sumOddLengthSubarrays(self, arr: list[int]) -> int:
        
        n = len(arr)
        total_sum = 0
        
        for i in range(n):
            
            # Combinatorics: How many start and end boundaries can surround this index
            left_choices = i + 1
            right_choices = n - i
            
            total_subarrays = left_choices * right_choices
            
            # Exactly half (rounded up) of the combinations produce an odd length
            odd_subarrays = (total_subarrays + 1) // 2
            
            # Mathematical contribution to the grand total
            total_sum += arr[i] * odd_subarrays
            
        return total_sum

"""
WHY EACH PART:
- (i + 1): Represents the number of elements to the left of `i` including `i` itself.
- (n - i): Represents the number of elements to the right of `i` including `i` itself.
- (total_subarrays + 1) // 2: This beautifully avoids any conditional `if` checks for parity. If total is 9, (9+1)//2 = 5. If total is 8, (8+1)//2 = 4. It naturally simulates the alternating odd/even distribution.
- total_sum += arr[i] * odd_subarrays: We skip looping through the actual items. We simply inject the mathematical weight of the number directly into the answer.

HOW IT WORKS (Example: arr = [10]):
i = 0, n = 1
left = 1, right = 1. total = 1.
odd = (1 + 1) // 2 = 1.
total_sum += 10 * 1 = 10.
Returns 10. ✓

KEY TECHNIQUE:
- Combinatorics
- Mathematical Element Contribution
- Constant Time Parity Logic

EDGE CASES:
- Smallest array length (n=1): Calculates properly without index out of bounds. ✓
- Array of identical numbers: The combinatorial logic depends solely on indices, so duplicate numbers don't confuse the engine. ✓

TIME COMPLEXITY: O(N) - We perform a single traversal of the array. The internal combinatorial calculations are basic arithmetic executed in strictly O(1) time.
SPACE COMPLEXITY: O(1) - No physical subarrays are ever created or stored in memory. We only allocate a handful of integer variables.
"""

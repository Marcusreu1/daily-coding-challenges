# 1799. Maximize Score After N Operations
# Difficulty: Hard
# https://leetcode.com/problems/maximize-score-after-n-operations/

"""
PROBLEM:
You are given nums, an array of positive integers of size 2 * n. You must perform n operations on this array.
In the ith operation (1-indexed), you will:
- Choose two elements, x and y.
- Receive a score of i * gcd(x, y).
- Remove x and y from nums.
Return the maximum score you can receive after performing n operations.

EXAMPLES:
Input: nums = [1,2] → Output: 1
Explanation: The optimal choice of operations is:
(1 * gcd(1, 2)) = 1 * 1 = 1

Input: nums = [3,4,6,8] → Output: 11
Explanation: The optimal choice of operations is:
1. Choose 3 and 6, receive 1 * gcd(3, 6) = 1 * 3 = 3
2. Choose 4 and 8, receive 2 * gcd(4, 8) = 2 * 4 = 8
Total score = 3 + 8 = 11.

CONSTRAINTS:
- 1 <= n <= 7
- nums.length == 2 * n
- 1 <= nums[i] <= 10^6

ALGORITHM RULES (BITMASK DYNAMIC PROGRAMMING):
Since the maximum length of nums is 14 (2 * 7), we can represent the state of the array (which elements have been used) using a 14-bit integer (bitmask).
- A bit '0' means the element at that index is available.
- A bit '1' means the element has been used.
We use a recursive function with memoization to explore all valid pairs of unused elements.
For every valid pair, we calculate the score: operation_number * gcd(num1, num2), and recursively solve for the remaining available elements.
We cache the maximum score for each bitmask to avoid redundant calculations.

VISUALIZATION (nums = [1, 2, 3, 4], n = 2):
Initial mask: 0000 (all available)

Pick index 0 and 1 (values 1, 2):
- Score = 1 * gcd(1, 2) = 1
- New mask: 0011
- Recursive call with mask 0011, op 2 -> picks index 2 and 3 (values 3, 4)
- Score = 2 * gcd(3, 4) = 2 * 1 = 2
- Total = 1 + 2 = 3

Pick index 0 and 2 (values 1, 3):
- Score = 1 * gcd(1, 3) = 1
- New mask: 0101
- Recursive call with mask 0101, op 2 -> picks index 1 and 3 (values 2, 4)
- Score = 2 * gcd(2, 4) = 2 * 2 = 4
- Total = 1 + 4 = 5 (Max score found!) ✓
"""

import math
from typing import List

# STEP 1: Initialize a memoization dictionary to cache states.
# STEP 2: Create a helper recursive function that takes the current bitmask and operation number.
# STEP 3: Base case: If the mask indicates all elements are used, return 0.
# STEP 4: Iterate through all possible unused pairs (i, j) using bitwise checks.
# STEP 5: For each pair, calculate the score, generate the new mask, and recursively find the future score.
# STEP 6: Store and return the maximum score for the current mask.

class Solution:
    def maxScore(self, nums: List[int]) -> int:
        
        n_elements = len(nums)
        memo = {}
        
        def dfs(mask: int, op_number: int) -> int:
            
            # Base case: All elements are used (mask is fully 1s)
            if mask == (1 << n_elements) - 1:
                return 0
                
            # Return cached result if this state has been computed before
            if mask in memo:
                return memo[mask]
                
            max_score = 0
            
            # Iterate through all combinations to find pairs
            for i in range(n_elements):
                # Check if the i-th element is already used in the mask
                if (mask >> i) & 1:
                    continue
                    
                for j in range(i + 1, n_elements):
                    # Check if the j-th element is already used in the mask
                    if (mask >> j) & 1:
                        continue
                        
                    # Both i and j are available. Create the new state mask by setting their bits to 1
                    new_mask = mask | (1 << i) | (1 << j)
                    
                    # Calculate the score for picking elements i and j at the current operation step
                    current_score = op_number * math.gcd(nums[i], nums[j])
                    
                    # Add future max score recursively
                    total_score = current_score + dfs(new_mask, op_number + 1)
                    
                    # Update the maximum score found for this specific mask
                    max_score = max(max_score, total_score)
                    
            # Cache the optimal result for this bitmask state
            memo[mask] = max_score
            return max_score

        # Start the recursion with an empty mask (0) and operation number 1
        return dfs(0, 1)

"""
WHY EACH PART:
- mask == (1 << n_elements) - 1: The bitwise shift creates a binary number with a 1 at the n-th position. Subtracting 1 flips all lower bits to 1s. This efficiently checks if the array is fully used.
- (mask >> i) & 1: Shifts the mask so the i-th bit is at the 0th position, then performs a bitwise AND. It returns 1 if the item was used, 0 if available.
- mask | (1 << i) | (1 << j): Bitwise OR strictly forces the i-th and j-th bits to become 1, updating our state without mutating arrays.
- math.gcd: Highly optimized C-backend Python function for calculating the Greatest Common Divisor.

HOW IT WORKS (Example: nums = [1, 2]):

Initial: mask = 0 (binary 00), op_number = 1

Iteration (i=0, j=1):
├── check i: (0 >> 0) & 1 = 0 (Available)
├── check j: (0 >> 1) & 1 = 0 (Available)
├── new_mask = 0 | (1 << 0) | (1 << 1) = 0 | 1 | 2 = 3 (binary 11)
├── current_score = 1 * gcd(1, 2) = 1 * 1 = 1
└── recursive call: dfs(3, 2)
    └── mask 3 == (1 << 2) - 1 -> 3 == 3. Returns 0.
├── total_score = 1 + 0 = 1
└── max_score = max(0, 1) = 1

Exit: memo[0] = 1

return 1 ✓

KEY TECHNIQUE:
- Bitmasking: Using integers as ultra-lightweight sets to track used/unused elements.
- Dynamic Programming with Memoization (Top-Down): Pruning overlapping subproblems (e.g., picking A then B leaves the exact same remaining pool as picking B then A).

EDGE CASES:
- Smallest constraints (n=1, length 2): Immediately grabs the only pair, calculates score, and finishes in O(1).
- Large primes: math.gcd handles relatively prime numbers instantly by returning 1.

TIME COMPLEXITY: O(2^N * N^2) - Where N is the array length (max 14). There are 2^14 (16,384) possible bitmask states. For each state, we loop roughly 14*13/2 = 91 times. ~1.5 million operations, which is extremely fast.
SPACE COMPLEXITY: O(2^N) - The memoization dictionary will store at most 16,384 states, requiring negligible memory.

CONCEPTS USED:
- Bitmasking
- Dynamic Programming (Memoization)
- Mathematical Algorithms (GCD)
- Combinatorics
"""

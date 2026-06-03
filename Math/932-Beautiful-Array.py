# 932. Beautiful Array
# Difficulty: Medium
# https://leetcode.com/problems/beautiful-array/

"""
PROBLEM:
An array `nums` of length `n` is beautiful if it is a permutation of the integers 1 to n, and:
For every i < j, there is no index k with i < k < j where 2 * nums[k] == nums[i] + nums[j].
Given the integer n, return any beautiful array nums of length n. There will be at least one valid answer for the given n.

EXAMPLES:
Input: n = 4
Output: [2,1,4,3] (Other valid answers exist, such as [1,3,2,4])

Input: n = 5
Output: [3,1,2,5,4] (Other valid answers exist, such as [1,5,3,2,4])

CONSTRAINTS:
- 1 <= n <= 1000

MATHEMATICAL REDUCTION:
The condition 2 * nums[k] == nums[i] + nums[j] implies that nums[i] and nums[j] cannot have nums[k] as their exact arithmetic mean if k is between them.
Notice that the left side of the equation (2 * nums[k]) is ALWAYS EVEN.
To ensure the equation is never true, we can force the right side (nums[i] + nums[j]) to ALWAYS BE ODD.
The sum of two integers is odd if and only if one is ODD and the other is EVEN.
Therefore, if we place all ODD numbers on the left half of the array, and all EVEN numbers on the right half, no cross-boundary pair will ever violate the rule.

Furthermore, the "beautiful" property is preserved under linear transformations. 
If array A is beautiful:
- The array [2*x - 1 for x in A] (Odd numbers) is also beautiful.
- The array [2*x for x in A] (Even numbers) is also beautiful.
We can iteratively build the array from the base case [1].

VISUALIZATION (Building up to n = 5):
Start: [1]

Iteration 1:
├── Odds:  2(1)-1 = [1]
├── Evens: 2(1)   = [2]
└── Merge: [1, 2]

Iteration 2:
├── Odds:  2(1)-1=1, 2(2)-1=3 -> [1, 3]
├── Evens: 2(1)=2, 2(2)=4     -> [2, 4]
└── Merge: [1, 3, 2, 4]

Iteration 3:
├── Odds:  [2(1)-1, 2(3)-1, 2(2)-1, 2(4)-1] -> [1, 5, 3, 7]
├── Evens: [2(1), 2(3), 2(2), 2(4)]         -> [2, 6, 4, 8]
├── Merge: [1, 5, 3, 7, 2, 6, 4, 8]
└── Filter: Keep only elements <= 5 -> [1, 5, 3, 2, 4]

Result: [1, 5, 3, 2, 4] ✓
"""

# STEP 1: Initialize the base case array with just [1]
# STEP 2: Use a while loop to expand the array until it contains 'n' elements
# STEP 3: Generate the left half by applying 2x - 1 to current elements (Odds), filtering out values > n
# STEP 4: Generate the right half by applying 2x to current elements (Evens), filtering out values > n
# STEP 5: Merge both halves to form the new beautiful array for the next iteration

class Solution:
    def beautifulArray(self, n: int) -> list[int]:
        
        res = [1]                                                              # Base case beautiful array
        
        while len(res) < n:                                                    # Expand until we reach target length
            
            odds = [2 * x - 1 for x in res if 2 * x - 1 <= n]                  # Transform to odds and filter
            evens = [2 * x for x in res if 2 * x <= n]                         # Transform to evens and filter
            
            res = odds + evens                                                 # Combine odds (left) and evens (right)
            
        return res                                                             # Return the fully built beautiful array

"""
WHY EACH PART:
- res = [1]: 1 is a valid permutation of length 1, containing no i < k < j violations. It acts as our mathematical seed.
- 2 * x - 1 and 2 * x: These linear transformations map our base sequence into non-overlapping odd and even domains while perfectly preserving the relative distances that prevent arithmetic progression violations.
- if <= n: Because we double the span of our array on each iteration, we will overshoot 'n' if 'n' is not a perfect power of 2. Filtering out out-of-bounds numbers does not break the beautiful property.

HOW IT WORKS (Example: n = 4):

Initial State:
├── res = [1]
├── n = 4

Loop 1 (len(res) < 4):
├── odds = [2*1 - 1] = [1]
├── evens = [2*1] = [2]
└── res = [1, 2]

Loop 2 (len(res) < 4):
├── odds = [2*1 - 1, 2*2 - 1] = [1, 3]
├── evens = [2*1, 2*2] = [2, 4]
└── res = [1, 3, 2, 4]

Exit loop (len(res) == 4)
return [1, 3, 2, 4] ✓

KEY TECHNIQUE:
- Divide and Conquer + Mathematical Transformation. By separating the problem into odd and even domains, we eliminate the core conflict (even sums crossing the middle). The bottom-up approach iteratively scales a known valid state into the target state.

EDGE CASES:
- n = 1: The while loop condition (len(res) < 1) evaluates to False immediately. Returns [1]. ✓
- n is not a power of 2: The inline filtering (if <= n) gracefully removes excess numbers generated during the scaling phases without disrupting the internal valid sequences. ✓

TIME COMPLEXITY: O(N log N) - In each iteration, the length of `res` effectively doubles. There are roughly log2(N) iterations, and creating the new lists takes time proportional to the current length.
SPACE COMPLEXITY: O(N) - The array `res` holds exactly N elements at the end, and the temporary `odds` and `evens` lists take up to N space combined.

CONCEPTS USED:
- Divide and Conquer
- Array / Mathematics
- Recursion / Iterative Bottom-Up Build
"""

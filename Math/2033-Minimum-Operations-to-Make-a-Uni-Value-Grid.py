# 2033. Minimum Operations to Make a Uni-Value Grid
# Difficulty: Medium
# https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/

"""
PROBLEM:
You are given a 2D integer grid of size m x n and an integer x. In one operation, you can add x to or subtract x from any element in the grid.
A uni-value grid is a grid where all the elements of it are equal.
Return the minimum number of operations to make the grid uni-value. If it is not possible, return -1.

EXAMPLES:
Input: grid = [[2,4],[6,8]], x = 2 → Output: 4
Explanation: We can make every element equal to 4 by doing the following: 
- grid[0][0] = 2. Add 2 -> 4 (1 operation)
- grid[0][1] = 4. No operations needed.
- grid[1][0] = 6. Subtract 2 -> 4 (1 operation)
- grid[1][1] = 8. Subtract 2 twice -> 4 (2 operations)
Total operations = 1 + 0 + 1 + 2 = 4.

Input: grid = [[1,5],[2,3]], x = 1 → Output: 5
Explanation: We can make every element equal to 3.

Input: grid = [[1,2],[3,4]], x = 2 → Output: -1
Explanation: It is impossible to make every element equal. 

CONSTRAINTS:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10^5
- 1 <= grid[i][j], x <= 10^4

MATH RULES (MODULO EQUIVALENCE & MEDIAN OPTIMIZATION):
1. Feasibility (Modulo): Two numbers 'a' and 'b' can only be made equal by adding/subtracting 'x' if they belong to the same equivalence class modulo 'x'. Mathematically, a % x == b % x. If this is violated anywhere in the grid, return -1.
2. Optimality (Median): To minimize the sum of absolute deviations (the total operations), all numbers should converge to the MEDIAN of the dataset, not the mean. The median mathematically guarantees the shortest total travel distance for 1D coordinate points.

VISUALIZATION (grid = [[1, 5, 9]], x = 4):
Flatten: [1, 5, 9]
Check feasibility: 
1 % 4 = 1
5 % 4 = 1
9 % 4 = 1
All match. It is possible.

Find Median:
Sorted array: [1, 5, 9]. Median is at index 1 -> value 5.

Calculate Operations:
- Distance from 1 to 5 is 4. Operations = 4 / x = 4 / 4 = 1
- Distance from 5 to 5 is 0. Operations = 0 / 4 = 0
- Distance from 9 to 5 is 4. Operations = 4 / 4 = 1
Total = 2 ✓
"""

from typing import List

# STEP 1: Flatten the 2D grid into a 1D list for easier sorting and processing.
# STEP 2: Establish a baseline modulo using the first element to check feasibility.
# STEP 3: Iterate through the flat list. If any number violates the modulo baseline, return -1.
# STEP 4: Sort the list to easily locate the mathematical median.
# STEP 5: Calculate the exact operations required for each number to reach the median and sum them up.

class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        
        # Flatten the matrix into a single 1D array using list comprehension
        nums = [val for row in grid for val in row]
        
        # Determine the required remainder for all elements
        baseline_mod = nums[0] % x
        
        # Check if it's mathematically possible to unify all values
        for num in nums:
            if num % x != baseline_mod:
                return -1
                
        # Sort the array to find the median
        nums.sort()
        
        # The median minimizes the sum of absolute distances
        mid_index = len(nums) // 2
        median = nums[mid_index]
        
        total_operations = 0
        
        # Accumulate the required operations (distance / x)
        for num in nums:
            total_operations += abs(num - median) // x
            
        return total_operations

"""
WHY EACH PART:
- [val for row in grid for val in row]: Pythonic way to flatten a 2D matrix into a 1D list in O(M*N) time, removing structural complexity.
- num % x != baseline_mod: Fast O(N) short-circuit evaluation. Prevents wasting time sorting the array if the grid is fundamentally invalid.
- nums[len(nums) // 2]: Grabs the median in O(1) time after sorting. (For arrays with an even length, either of the two middle elements works mathematically, integer division elegantly defaults to the right one).
- abs(num - median) // x: Calculates exactly how many 'x' steps are needed to cross the distance between the current number and the median.

KEY TECHNIQUE:
- Statistical Optimization: Relying on the Median theorem for L1 norm optimization (Manhattan distance / absolute deviations).
- Modulo Arithmetic: Using remainders to evaluate reachability across discrete jumps.

EDGE CASES:
- Grid with only 1 element (1x1): The loop succeeds, sorting takes 0 time, median is the element itself. abs(num-median) is 0. Returns 0 operations perfectly.
- Already unified grid (e.g., all 5s): Baseline modulo matches, median is 5, distance is 0. Returns 0 correctly.

TIME COMPLEXITY: O(K log K) - Where K is the total number of elements (M * N). Flattening and iterating take O(K), but Python's Timsort algorithm dominates with O(K log K).
SPACE COMPLEXITY: O(K) - We allocate a new 1D array of size M * N to hold the flattened grid for sorting.
"""

# 1131. Maximum of Absolute Value Expression
# Difficulty: Medium
# https://leetcode.com/problems/maximum-of-absolute-value-expression/

"""
PROBLEM:
Given two arrays of integers with equal lengths, return the maximum value of:
|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|
where the maximum is taken over all 0 <= i, j < arr1.length.

EXAMPLES:
Input: arr1 = [1,2,3,4], arr2 = [-1,4,5,6]
Output: 13

Input: arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]
Output: 20

CONSTRAINTS:
- 2 <= arr1.length == arr2.length <= 40000
- -10^6 <= arr1[i], arr2[i] <= 10^6

MATHEMATICAL INTUITION (THE "TRICK"):
The naive approach uses nested loops to test all (i, j) pairs. 
Since N = 40,000, N^2 is 1.6 billion operations, causing a Time Limit Exceeded (TLE) error.

We must eliminate the nested loop. The hurdle is the absolute value `|x|`, which branches into `x` or `-x`.
If we expand the expression `|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|`, 
removing the absolute values creates 8 possible mathematical sign combinations (+ or - for each term).
Since `|i - j|` is symmetric and we are looking for the maximum difference, we can assume `i > j`, 
which means `|i - j|` is always `i - j`. This reduces our combinations to 4 scenarios:

1. (arr1[i] + arr2[i] + i) - (arr1[j] + arr2[j] + j)
2. (arr1[i] - arr2[i] + i) - (arr1[j] - arr2[j] + j)
3. (-arr1[i] + arr2[i] + i) - (-arr1[j] + arr2[j] + j)
4. (-arr1[i] - arr2[i] + i) - (-arr1[j] - arr2[j] + j)

Notice the profound transformation: We completely separated the `i` terms from the `j` terms!
For any of these 4 equations, we just compute its value for every index `k`. 
To maximize the difference, we just subtract the minimum value from the maximum value in that array.
"""

# STEP 1: Create arrays to store the results of the 4 algebraic equations.
# STEP 2: Iterate through the arrays once (O(N) time).
# STEP 3: Apply the 4 formulas to the current index and store the results.
# STEP 4: For each of the 4 resulting arrays, find the max difference (max(array) - min(array)).
# STEP 5: Return the highest maximum difference among the 4 scenarios.

from typing import List

class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        
        n = len(arr1)
        
        # Arrays to hold the evaluated values for the 4 unwrapped algebraic scenarios
        v1, v2, v3, v4 = [], [], [], []
        
        # Step 2 & 3: Group terms by single index to drop the O(N^2) complexity
        for i in range(n):
            v1.append(arr1[i] + arr2[i] + i)
            v2.append(arr1[i] - arr2[i] + i)
            v3.append(-arr1[i] + arr2[i] + i)
            v4.append(-arr1[i] - arr2[i] + i)
            
        # Helper function to find the maximum possible difference in a single scenario
        def get_max_diff(scenario_values: List[int]) -> int:
            return max(scenario_values) - min(scenario_values)
            
        # Step 4 & 5: Calculate the max difference for each scenario and return the absolute maximum
        return max(
            get_max_diff(v1),
            get_max_diff(v2),
            get_max_diff(v3),
            get_max_diff(v4)
        )

"""
WHY EACH PART:
- Unwrapping absolute values: The core mathematical strategy to break the dependency between i and j.
- Grouping: Turning (A_i - A_j) into (A_i + B_i + i) - (A_j + B_j + j) allows us to compute properties for a single element independently.
- max() - min(): If you have an array of values, the largest distance between any two elements is always the largest element minus the smallest element.

HOW IT WORKS (Conceptual):
Instead of comparing Element 1 with Element 2, Element 3, Element 4...
We assign a "score" to every element based on 4 different rating systems (the 4 equations).
We then look at the highest scorer and lowest scorer in System 1, System 2, System 3, and System 4.
The biggest gap found in any system is our guaranteed absolute maximum.

TIME COMPLEXITY: O(N) - We iterate through the arrays exactly once to build our 4 lists. Finding min/max takes O(N). We reduced a 1.6 billion operation task to a ~40,000 operation task.
SPACE COMPLEXITY: O(N) - We store 4 arrays of size N. (Note: This can be optimized to O(1) by only tracking the running min and max, but O(N) arrays make the mathematical logic significantly clearer).

CONCEPTS USED:
- Math (Absolute Value Properties)
- Distributive Property
- Manhattan Distance equivalent in 3D Space
"""

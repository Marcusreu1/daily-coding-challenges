# 2358. Maximum Number of Groups Entering a Competition
# Difficulty: Medium
# https://leetcode.com/problems/maximum-number-of-groups-entering-a-competition/

"""
PROBLEM:
You are given a positive integer array grades which represents the grades of students in a university. You would like to enter all these students into a competition in ordered non-empty groups.
The grading rules strictly require that for every group i (where 1 <= i < k):
- The size of group i is strictly less than the size of group i+1.
- The sum of grades of group i is strictly less than the sum of grades of group i+1.
Return the maximum number of groups that can be formed.

EXAMPLES:
Input: grades = [10,6,12,7,3,5] → Output: 3
Explanation: We can form 3 groups: [10], [3,12], [5,6,7].
Sizes: 1 < 2 < 3. Sums: 10 < 15 < 18. Both conditions met.

Input: grades = [8,8] → Output: 1
Explanation: We can only form 1 group [8,8] since forming 2 groups [8] and [8] violates the strictly increasing size rule (1 is not strictly less than 1).

CONSTRAINTS:
- 1 <= grades.length <= 10^5
- 1 <= grades[i] <= 10^5

MATH RULES (DATA IRRELEVANCE & QUADRATIC TRIANGULAR INVERSE):
1. Data Irrelevance: To maximize the number of groups, we must minimize their sizes. The most optimal size progression is 1, 2, 3, 4... K. If we were to sort the array and assign the lowest grades to the smallest groups and the highest grades to the largest groups, the sum condition is trivially satisfied simply because K+1 positive numbers will always sum to more than K positive numbers from the same sorted sequence. Therefore, the actual grades are computationally irrelevant; only the length N of the array dictates the result.
2. Quadratic Inverse: The progression of group sizes forms a Gaussian sum (Triangular Number): K * (K + 1) / 2 <= N.
   Solving for K algebraically:
   K^2 + K - 2N <= 0
   Using the quadratic formula: K = (sqrt(1 - 4(1)(-2N)) - 1) / 2
   K = (sqrt(8N + 1) - 1) / 2.
"""

from typing import List

# STEP 1: Extract the length of the array, completely bypassing the values inside.
# STEP 2: Apply the quadratic formula derived from the Triangular Numbers inequality.
# STEP 3: Truncate to an integer to resolve the maximum complete progression and return.

class Solution:
    def maximumGroups(self, grades: List[int]) -> int:
        
        # The algorithm purely depends on the total count of elements
        n = len(grades)
        
        # O(1) Mathematical Resolution
        return int(((8 * n + 1) ** 0.5 - 1) // 2)

"""
WHY EACH PART:
- len(grades): A pure O(1) property lookup in Python, avoiding simulating, parsing, or sorting the elements.
- ** 0.5: Calculates the square root in constant time via the hardware's floating-point unit (FPU).
- // 2: Floor division ensures that if we have leftovers that cannot form a full new sequential group, they are logically absorbed into the final group without affecting the max group count.

KEY TECHNIQUE:
- Algebraic Reduction: Realizing that a complex combinatorial partitioning problem is fundamentally constrained by a static algebraic inequality, allowing us to drop the Time Complexity from O(N log N) to O(1).

EDGE CASES:
- n = 1 or n = 2: Math evaluates to 1. Correct, as a progression of 1, 2 needs at least 3 elements.
- Extremely large array (10^5): Avoids Time Limit Exceeded instantly. Precision loss is non-existent as the values are well within the 2^53 safe integer threshold for double-precision floats.

TIME COMPLEXITY: O(1) - The array is never traversed or sorted. A single mathematical equation executes instantaneously.
SPACE COMPLEXITY: O(1) - Only the integer property of the list length is processed.
"""

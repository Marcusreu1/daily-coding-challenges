# 976. Largest Perimeter Triangle
# Difficulty: Easy
# https://leetcode.com/problems/largest-perimeter-triangle/

"""
PROBLEM:
Given an integer array `nums`, return the largest perimeter of a triangle with a non-zero area, formed from three of these lengths.
If it is impossible to form any triangle of a non-zero area, return 0.

EXAMPLES:
Input: nums = [2,1,2]
Output: 5 (Lengths 2, 1, and 2 can form a triangle: 2 + 1 > 2. Perimeter = 5).

Input: nums = [1,2,1,10]
Output: 0 (You cannot form any valid triangle from these lengths).

CONSTRAINTS:
- 3 <= nums.length <= 10^4
- 1 <= nums[i] <= 10^6

MATHEMATICAL REDUCTION:
For any three positive lengths a, b, and c where a <= b <= c, they can form a valid triangle if and only if:
a + b > c  (Triangle Inequality Theorem)

To maximize the perimeter, we should evaluate the longest available sides first. 
If we sort the array in descending order, we can check adjacent triplets (c, b, a). 
Because the array is sorted, the first triplet that satisfies b + a > c will definitively yield the maximum possible perimeter.

VISUALIZATION (nums = [3, 2, 3, 4]):
Sort descending: [4, 3, 3, 2]

Iteration 1 (checking indices 0, 1, 2):
Sides: c = 4, b = 3, a = 3
Condition: 3 + 3 > 4 ? -> 6 > 4 -> True!
Perimeter: 4 + 3 + 3 = 10

Since we checked the largest elements first, 10 is guaranteed to be the largest perimeter.

Result: 10 ✓
"""

# STEP 1: Sort the array in descending order to prioritize the largest possible perimeters.
# STEP 2: Iterate through the array, sliding a window of 3 elements at a time.
# STEP 3: Apply the Triangle Inequality Theorem to the triplet.
# STEP 4: Return the sum of the first valid triplet found.
# STEP 5: If the loop finishes without finding a valid triplet, return 0.

class Solution:
    def largestPerimeter(self, nums: list[int]) -> int:
        
        nums.sort(reverse=True)                                                # Sort lengths from largest to smallest
        
        for i in range(len(nums) - 2):                                         # Loop leaving room for a 3-element window
            
            c = nums[i]                                                        # Largest side of the current triplet
            b = nums[i+1]                                                      # Middle side
            a = nums[i+2]                                                      # Smallest side
            
            if b + a > c:                                                      # Triangle Inequality Theorem check
                return c + b + a                                               # Return perimeter immediately
                
        return 0                                                               # Impossible to form a triangle

"""
WHY EACH PART:
- nums.sort(reverse=True): Setting `reverse=True` allows us to start checking the absolute largest candidates immediately, making the algorithm greedy.
- range(len(nums) - 2): We stop 2 elements before the end of the array to prevent an IndexError when accessing i+1 and i+2.
- if b + a > c: We only need to check this single condition. Since the array is sorted descending (c >= b >= a), we already mathematically know that c + a > b and c + b > a.
- return c + b + a: The greedy approach ensures that the first valid triangle encountered has the maximal perimeter, so we break and return instantly.

HOW IT WORKS (Example: [1, 2, 1, 10]):

Initial State:
├── nums = [1, 2, 1, 10]
└── nums.sort() -> [10, 2, 1, 1]

Iteration 1 (i = 0):
├── c = 10, b = 2, a = 1
├── Condition: 2 + 1 > 10 ? -> 3 > 10 -> False
└── Move to next triplet.

Iteration 2 (i = 1):
├── c = 2, b = 1, a = 1
├── Condition: 1 + 1 > 2 ? -> 2 > 2 -> False
└── Move to next triplet.

Exit loop: (Checked all triplets, none valid).
return 0 ✓

KEY TECHNIQUE:
- Greedy Algorithm + Sorting. By sorting the data, we transform an O(N^3) brute-force combination problem into an elegant O(N log N) linear scan.

EDGE CASES:
- No valid triangles (e.g., [1, 2, 1]): The condition is never met, safely falls back to returning 0. ✓
- Minimum array length (3 elements): The loop runs exactly once. Checks the only possible combination. ✓
- Duplicated values (e.g., [3, 3, 3]): 3 + 3 > 3 is True. Equilateral triangles are handled perfectly. ✓

TIME COMPLEXITY: O(N log N) - Sorting the array takes O(N log N) time. The subsequent linear scan takes O(N) time at worst. The sort dominates the complexity.
SPACE COMPLEXITY: O(1) or O(N) - Depends on the sorting algorithm implementation in Python (Timsort takes O(N) auxiliary space in the worst case, but the logic itself uses O(1) extra space).

CONCEPTS USED:
- Arrays
- Greedy Algorithm
- Sorting
- Geometry / Mathematics
"""

# 1806. Minimum Number of Operations to Reinitialize a Permutation
# Difficulty: Medium
# https://leetcode.com/problems/minimum-number-of-operations-to-reinitialize-a-permutation/

"""
PROBLEM:
You are given an even integer n. You initially have a permutation perm of size n where perm[i] == i (0-indexed).
In one operation, you will create a new array arr, and for each i:
- If i % 2 == 0, then arr[i] = perm[i / 2].
- If i % 2 == 1, then arr[i] = perm[n / 2 + (i - 1) / 2].
You will then assign perm = arr.
Return the minimum non-zero number of operations you need to perform on perm to return the permutation to its initial value.

EXAMPLES:
Input: n = 4 → Output: 2
Explanation: perm = [0,1,2,3] initially.
After the 1st operation, perm = [0,2,1,3]
After the 2nd operation, perm = [0,1,2,3]
So it takes only 2 operations.

Input: n = 6 → Output: 4
Explanation: perm = [0,1,2,3,4,5]
1st: [0,3,1,4,2,5]
2nd: [0,4,3,2,1,5]
3rd: [0,2,4,1,3,5]
4th: [0,1,2,3,4,5]

CONSTRAINTS:
- 2 <= n <= 1000
- n is even.

MATH RULES (PERMUTATION CYCLES & GROUP THEORY):
Instead of simulating the entire array, which is memory and time-consuming, we can track a single element.
Elements 0 and n-1 never move. The element initially at index 1 drives the maximal cycle length of this specific permutation.
When the element starting at index 1 returns to index 1, the entire array is mathematically guaranteed to be fully restored.

By reversing the given logic, we can track where the element currently at index 'x' goes in the next step:
- If x < n / 2, it moves to: x * 2
- If x >= n / 2, it moves to: (x - n / 2) * 2 + 1

VISUALIZATION (n = 6):
Track the element initially at index 1.
Initial: pos = 1, ops = 0

Turn 1: pos (1) < 3 -> pos = 1 * 2 = 2. (ops = 1)
Turn 2: pos (2) < 3 -> pos = 2 * 2 = 4. (ops = 2)
Turn 3: pos (4) >= 3 -> pos = (4 - 3) * 2 + 1 = 3. (ops = 3)
Turn 4: pos (3) >= 3 -> pos = (3 - 3) * 2 + 1 = 1. (ops = 4)

pos is back to 1. Stop. Total ops = 4 ✓
"""

# STEP 1: Initialize current position at 1 and operation counter at 0.
# STEP 2: Use an infinite loop to simulate the position jumps.
# STEP 3: Apply the position tracking formulas based on whether the position is in the first or second half.
# STEP 4: Increment the operation counter.
# STEP 5: Break the loop if the position returns to 1 and return the counter.

class Solution:
    def reinitializePermutation(self, n: int) -> int:
        
        # Edge case optimization: If n is 2, it only takes 1 operation to reinitialize.
        if n == 2:
            return 1
            
        current_pos = 1
        operations = 0
        half_n = n // 2
        
        while True:
            # Calculate the next index for the element currently at 'current_pos'
            if current_pos < half_n:
                current_pos = current_pos * 2
            else:
                current_pos = (current_pos - half_n) * 2 + 1
                
            operations += 1
            
            # If the tracked element returns to its starting position, the whole array is restored
            if current_pos == 1:
                break
                
        return operations

"""
WHY EACH PART:
- current_pos = 1: Index 1 is the most dynamic anchor in this permutation sequence.
- half_n = n // 2: Caching the midpoint prevents recalculating division in every loop iteration.
- if current_pos == 1: Acts as the loop breaker, relying on the guarantee of group theory that the array is perfectly cyclic.

KEY TECHNIQUE:
- Group Theory Tracking: Bypassing full state simulation (arrays) to track the cycle of a single representative element.
- Space Complexity Optimization: Transforming an O(N) space problem into an O(1) space solution.

EDGE CASES:
- n = 2: Triggers the immediate early return, correctly giving 1 operation without iterating.

TIME COMPLEXITY: O(N) - The maximum length of a permutation cycle for this problem is strictly less than N. The loop executes at most N times.
SPACE COMPLEXITY: O(1) - We only track integer variables (current_pos, operations, half_n).
"""

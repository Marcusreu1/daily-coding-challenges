# 1551. Minimum Operations to Make Array Equal
# Difficulty: Medium
# https://leetcode.com/problems/minimum-operations-to-make-array-equal/

"""
PROBLEM:
You have an array `arr` of length `n` where `arr[i] = (2 * i) + 1` for all valid values of `i`.
In one operation, you can select two indices x and y where 0 <= x, y < n and subtract 1 from arr[x] and add 1 to arr[y] (The sum of the array elements stays the same). 
Return the minimum number of operations needed to make all the elements of arr equal.

EXAMPLES:
Input: n = 3
Output: 2
(Explanation: arr = [1, 3, 5]
First operation choose x=2 and y=0, this leads arr to be [2, 3, 4]
In the second operation choose x=2 and y=0 again, thus arr = [3, 3, 3].)

Input: n = 6
Output: 9
(Explanation: arr = [1, 3, 5, 7, 9, 11]. The target average is exactly 6.
Operations needed to bring [1, 3, 5] up to 6 are 5 + 3 + 1 = 9.)

CONSTRAINTS:
- 1 <= n <= 10^4

ALGORITHM LOGIC (O(1) Mathematical Abstraction):
1. By definition of the array generation `(2 * i) + 1`, the array forms an arithmetic progression of odd numbers.
2. Because it's perfectly symmetrical, the target value that all elements must reach (the mean) is exactly equal to `n`.
3. To find the total minimum operations, we only need to calculate how many additions the "left half" of the array needs to reach the target `n`.
4. If `n` is even, say `n = 2k`. The number of elements less than `n` is `k`. Their distances to `n` are consecutive odd numbers: 1, 3, 5, ..., 2k-1. The sum of the first `k` odd numbers is exactly `k^2`. Since `k = n/2`, the sum is (n/2)^2 = n^2 / 4.
5. If `n` is odd, say `n = 2k + 1`. The number of elements less than `n` is `k`. Their distances to `n` are consecutive even numbers: 2, 4, 6, ..., 2k. The sum of the first `k` even numbers is `k * (k + 1)`. Substituting `k = (n-1)/2`, it yields (n^2 - 1) / 4.
6. Using Python's floor division `//`, both the even and odd cases perfectly converge into a single, unified mathematical formula: (n * n) // 4.

VISUALIZATION (n = 5):
Array mathematically generated: [1, 3, 5, 7, 9]
Target to reach: 5

Left side distances to target:
- '1' needs 4 operations to become 5.
- '3' needs 2 operations to become 5.
Total operations = 4 + 2 = 6.

Unified Formula: (5 * 5) // 4 -> 25 // 4 -> 6. ✓
"""

# STEP 1: Derive the target equalizing value (which is conceptually `n`)
# STEP 2: Use the unified mathematical sum formula `(n * n) // 4` to bypass simulated loops
# STEP 3: Return the strictly calculated O(1) integer

class Solution:
    def minOperations(self, n: int) -> int:
        
        # O(1) Pattern Reduction (Sum of an Arithmetic Series logic)
        return (n * n) // 4

"""
WHY EACH PART:
- (n * n): Squares the length of the array, capturing the geometrical growth of the operations required.
- // 4: Floor division handles both Even and Odd parity cases flawlessly. For odd numbers (e.g., 25 // 4), it naturally discards the fraction (returning 6) simulating the exact offset behavior of the odd median.

HOW IT WORKS (Example: n = 4):
Array is logically [1, 3, 5, 7]. Target is 4.
Diffs for left half [1, 3] are 3 and 1. Sum is 4.
Formula: (4 * 4) // 4 -> 16 // 4 = 4. ✓

KEY TECHNIQUE:
- Mathematical Pattern Recognition
- Arithmetic Series Optimization
- Complete elimination of loops for O(1) execution

EDGE CASES:
- Minimum constraint (n = 1): Target is 1. Array is [1]. Needs 0 operations. (1 * 1) // 4 = 1 // 4 = 0. ✓
- Maximum constraint (n = 10000): Evaluates instantaneously as (10000^2 // 4 = 25000000) without running a 5,000-iteration loop. ✓

TIME COMPLEXITY: O(1) - Pure arithmetic evaluation. This is significantly faster and more scalable than simulating the array with an O(N) loop.
SPACE COMPLEXITY: O(1) - Absolute zero allocation. No array is ever generated in memory, saving O(N) space.
"""

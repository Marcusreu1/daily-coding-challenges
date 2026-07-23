# 1399. Count Largest Group
# Difficulty: Easy
# https://leetcode.com/problems/count-largest-group/

"""
PROBLEM:
Given an integer n. Each number from 1 to n is grouped according to the sum of its digits.
Return the number of groups that have the largest size.

EXAMPLES:
Input: n = 13
Output: 4
(Explanation: There are 9 groups in total, they are grouped according to sum of its digits of numbers from 1 to 13:
[1,10], [2,11], [3,12], [4,13], [5], [6], [7], [8], [9].
There are 4 groups with the largest size (which is 2).)

Input: n = 2
Output: 2
(Explanation: There are 2 groups [1], [2] of size 1. Both groups have the maximum size, so the total count is 2.)

CONSTRAINTS:
- 1 <= n <= 10^4

ALGORITHM LOGIC (Direct Array Mapping & Digit Extraction):
1. Since n <= 10000, the maximum possible digit sum is from the number 9999 (9+9+9+9 = 36).
2. We can use a fixed-size array of length 37 (indices 0 to 36) to count frequencies instead of a dynamic Hash Map. This saves overhead.
3. We loop through all numbers from 1 to n.
4. For each number, we extract its digits mathematically using modulo 10 and integer division by 10, summing them up.
5. We use the resulting sum as the exact index in our array and increment the count at that index.
6. After grouping, we find the maximum value present in the array (the largest group size).
7. We count how many times this maximum value appears in the array to find the number of tied largest groups.

VISUALIZATION (n = 13):
counts array (indices 1 to 9 shown): [..., 0, 0, 0, 0, 0, 0, 0, 0, 0, ...]

i = 1 to 9: Sums are 1 to 9. Array updates to:
counts = [..., 1, 1, 1, 1, 1, 1, 1, 1, 1, ...]

i = 10: Sum = 1+0 = 1. counts[1] += 1
i = 11: Sum = 1+1 = 2. counts[2] += 1
i = 12: Sum = 1+2 = 3. counts[3] += 1
i = 13: Sum = 1+3 = 4. counts[4] += 1

Final relevant array slice:
Index (Sum): 1  2  3  4  5  6  7  8  9
Size:        2  2  2  2  1  1  1  1  1

Max size is 2.
How many 2s are in the array? 4.
Return 4. ✓
"""

# STEP 1: Initialize a fixed-size array of 37 zeroes (since max sum of digits for 10000 is 36)
# STEP 2: Loop from 1 to n inclusively
# STEP 3: Mathematically calculate the sum of digits for the current number
# STEP 4: Use the sum as an index to increment the group size in the array
# STEP 5: Find the highest group size in the array using max()
# STEP 6: Return the total count of how many groups reached this maximum size

class Solution:
    def countLargestGroup(self, n: int) -> int:
        
        # Max sum is for 9999 -> 36. So 37 indices (0-36) are needed.
        counts = [0] * 37
        
        for i in range(1, n + 1):
            
            digit_sum = 0
            temp = i
            
            # Extract and sum digits mathematically
            while temp > 0:
                digit_sum += temp % 10                               # Extract last digit
                temp //= 10                                          # Remove last digit
                
            # Increment the group size for this specific digit sum
            counts[digit_sum] += 1
            
        # Identify the size of the largest group
        max_group_size = max(counts)
        
        # Count how many groups have this exact size
        return counts.count(max_group_size)

"""
WHY EACH PART:
- counts = [0] * 37: A highly optimized approach using Domain Knowledge. Since we definitively know the upper bound of the constraint (10^4), pre-allocating an array is significantly faster than using a dynamic dictionary.
- temp = i: We must not mutate our `i` iterator from the `for` loop, so we copy its value to a temporary variable to perform the mathematical reduction.
- max(counts): Python's built-in function heavily optimized in C to scan the tiny 37-element array instantly.
- counts.count(max_group_size): Once we know the target (e.g., the max size is 2), this native list method scans the array again to count how many indices achieved that exact value.

HOW IT WORKS (Example: n = 2):
Array initialized with zeroes.
i = 1 -> digit_sum = 1 -> counts[1] = 1
i = 2 -> digit_sum = 2 -> counts[2] = 1
max(counts) -> 1
counts.count(1) -> The number 1 appears twice (at index 1 and 2).
Returns 2. ✓

KEY TECHNIQUE:
- Direct Array Mapping (Histogramming)
- Base-10 Digit Extraction via Modulo Arithmetic

EDGE CASES:
- n = 1: Array updates only at index 1. max is 1. count is 1. Returns 1. ✓
- n = 10000: Max digit sum triggers exactly once (9999 = 36). Handled securely by the 37-element array limit without out-of-bounds errors. ✓

TIME COMPLEXITY: O(N * log10(N)) - We loop N times. Within the loop, the while loop runs proportionally to the number of digits in N, which is log10(N). For N=10000, it runs a max of 4 times per number. Effectively O(N).
SPACE COMPLEXITY: O(1) - The space used is strictly an array of 37 integers regardless of how large N grows. Strictly constant space.
"""

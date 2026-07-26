# 1414. Find the Minimum Number of Fibonacci Numbers Whose Sum Is K
# Difficulty: Medium
# https://leetcode.com/problems/find-the-minimum-number-of-fibonacci-numbers-whose-sum-is-k/

"""
PROBLEM:
Given an integer `k`, return the minimum number of Fibonacci numbers whose sum is equal to `k`. 
The same Fibonacci number can be used multiple times.
The Fibonacci numbers are defined as:
F_1 = 1
F_2 = 1
F_n = F_{n-1} + F_{n-2} for n > 2.

EXAMPLES:
Input: k = 7
Output: 2 
(Explanation: The Fibonacci numbers are: 1, 1, 2, 3, 5, 8, 13, ... 
For k = 7 we can use 2 + 5 = 7.)

Input: k = 10
Output: 2 
(Explanation: For k = 10 we can use 2 + 8 = 10.)

Input: k = 19
Output: 3 
(Explanation: For k = 19 we can use 1 + 5 + 13 = 19.)

CONSTRAINTS:
- 1 <= k <= 10^9

ALGORITHM LOGIC (Zeckendorf's Theorem & Greedy Approach):
1. Zeckendorf's theorem states that every positive integer can be represented as the sum of distinct non-consecutive Fibonacci numbers.
2. Because of this mathematical property, a pure Greedy Algorithm perfectly yields the minimum number of summands. 
3. We don't need Dynamic Programming. We simply always pick the largest possible Fibonacci number that is <= the remaining `k`.
4. Phase 1: Generate all Fibonacci numbers up to `k`. Because Fibonacci grows exponentially (Phi ~1.618), there are only about 44 Fibonacci numbers up to 10^9. This array is tiny.
5. Phase 2: Traverse the generated array backwards. If the current Fibonacci number fits into `k`, subtract it from `k` and increment our usage count.
6. Stop exactly when `k` reaches 0.

VISUALIZATION (k = 19):
Phase 1 (Generate):
fibs = [1, 1, 2, 3, 5, 8, 13] (Stop here because 13 + 8 = 21, which is > 19)

Phase 2 (Greedy Traverse Backwards):
Remaining k = 19
Check 13: 13 <= 19? Yes. k = 19 - 13 = 6. Count = 1.
Check  8:  8 <=  6? No.
Check  5:  5 <=  6? Yes. k = 6 - 5 = 1. Count = 2.
Check  3:  3 <=  1? No.
Check  2:  2 <=  1? No.
Check  1:  1 <=  1? Yes. k = 1 - 1 = 0. Count = 3.

k is 0. Loop ends. Return count (3). ✓
"""

# STEP 1: Initialize an array with the first two Fibonacci numbers [1, 1]
# STEP 2: Dynamically generate and append Fibonacci numbers as long as the next number is <= k
# STEP 3: Initialize a counter to track how many numbers we've used
# STEP 4: Iterate backwards through the generated Fibonacci array
# STEP 5: If the current Fibonacci number is <= k, subtract it from k and increment the counter
# STEP 6: Return the counter once k becomes 0

class Solution:
    def findMinFibonacciNumbers(self, k: int) -> int:
        
        # Phase 1: Generate Fibonacci sequence up to k
        fib_nums = [1, 1]
        
        # Calculate the next Fibonacci number by adding the last two elements
        while True:
            next_fib = fib_nums[-1] + fib_nums[-2]
            if next_fib > k:
                break
            fib_nums.append(next_fib)
            
        # Phase 2: Greedy subtraction from largest to smallest
        count = 0
        
        # Iterate from the end of the array to the beginning
        for i in range(len(fib_nums) - 1, -1, -1):
            
            # If the largest available Fibonacci fits in our remaining k
            if fib_nums[i] <= k:
                k -= fib_nums[i]                                     # Subtract it
                count += 1                                           # Record the usage
                
            # Early exit: if k is exhausted, we found our minimum sum
            if k == 0:
                break
                
        return count

"""
WHY EACH PART:
- next_fib = fib_nums[-1] + fib_nums[-2]: Python's negative indexing elegantly accesses the tail of the array to generate the sequence without needing independent variables.
- if next_fib > k: break: Prevents generating uselessly large numbers, strictly bounding our memory usage.
- for i in range(len(fib_nums) - 1, -1, -1): A standard reversed loop in Python. We must start from the largest number to satisfy the Greedy strategy mandated by Zeckendorf's theorem.
- if k == 0: break: Short-circuits the loop. Once the sum is perfectly matched, checking smaller Fibonacci numbers is mathematically pointless.

HOW IT WORKS (Example: k = 7):
fib_nums = [1, 1, 2, 3, 5]
Loop starts backwards at 5:
- Is 5 <= 7? Yes. k = 2. count = 1.
- Is 3 <= 2? No.
- Is 2 <= 2? Yes. k = 0. count = 2.
k == 0. Break loop.
Returns 2. ✓

KEY TECHNIQUE:
- Zeckendorf's Theorem (Mathematical foundation proving Greedy is optimal)
- Greedy Algorithm
- Dynamic Sequence Generation

EDGE CASES:
- k is an exact Fibonacci number (e.g., k = 8): Sequence generates up to 8. The loop evaluates 8 <= 8, k becomes 0, loop breaks. Returns 1. Works perfectly. ✓
- Maximum constraint (k = 10^9): Array reaches a maximum length of ~44 elements. The logic processes it in microseconds. ✓

TIME COMPLEXITY: O(log K) - The Fibonacci sequence grows exponentially, meaning the number of elements up to K is strictly proportional to log(K). Both generating the sequence and scanning it backwards take roughly ~45 iterations for K=10^9. Effectively, this runs in O(1) constant time relative to modern CPU limits.
SPACE COMPLEXITY: O(log K) - We store the Fibonacci numbers up to K in a list. For 10^9, this requires an array of size ~45, which takes a negligible, almost constant O(1) amount of memory space.
"""

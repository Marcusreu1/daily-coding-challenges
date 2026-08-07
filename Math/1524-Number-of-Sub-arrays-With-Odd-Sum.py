# 1524. Number of Sub-arrays With Odd Sum
# Difficulty: Medium
# https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/

"""
PROBLEM:
Given an array of integers `arr`, return the number of subarrays with an odd sum.
Since the answer can be very large, return it modulo 10^9 + 7.

EXAMPLES:
Input: arr = [1,3,5]
Output: 4
(Explanation: All subarrays are [[1],[1,3],[1,3,5],[3],[3,5],[5]].
All sub-arrays sum are [1,4,9,3,8,5].
Odd sums are [1,9,3,5] so the answer is 4.)

Input: arr = [2,4,6]
Output: 0
(Explanation: All subarrays sum are even, so the answer is 0.)

Input: arr = [1,2,3,4,5,6,7]
Output: 16

CONSTRAINTS:
- 1 <= arr.length <= 10^5
- 1 <= arr[i] <= 100

ALGORITHM LOGIC (Prefix Sums & Parity State Tracking):
1. Any contiguous subarray sum from index `i` to `j` is logically: prefix_sum[j] - prefix_sum[i-1].
2. For this subarray sum to be ODD, the two prefix sums must have DIFFERENT parities:
   - (Odd Prefix) - (Even Prefix) = Odd Subarray
   - (Even Prefix) - (Odd Prefix) = Odd Subarray
3. As we iterate through the array, we maintain a running `current_sum`.
4. We keep a tally of how many `even` and `odd` prefix sums we've encountered so far.
   - Note: The initial state before adding any numbers has a sum of 0 (which is Even). So `even_count` starts at 1.
5. If the `current_sum` is odd, it can pair with EVERY previously seen even prefix to form a valid odd subarray. We add `even_count` to our total.
6. If the `current_sum` is even, it pairs with EVERY previously seen odd prefix. We add `odd_count` to our total.
7. We apply the modulo 10^9 + 7 requirement at the end to prevent overflow in statically typed languages and satisfy the judge.

VISUALIZATION (arr = [1, 3, 5]):
Init: even_count=1, odd_count=0, ans=0, curr_sum=0

Num = 1: curr_sum = 1 (Odd). 
         Pairs with all previous evens -> ans += 1 (ans is 1)
         odd_count increments -> odd_count=1, even_count=1

Num = 3: curr_sum = 4 (Even). 
         Pairs with all previous odds -> ans += 1 (ans is 2)
         even_count increments -> odd_count=1, even_count=2

Num = 5: curr_sum = 9 (Odd). 
         Pairs with all previous evens -> ans += 2 (ans is 4)
         odd_count increments -> odd_count=2, even_count=2

Result = 4. ✓
"""

# STEP 1: Define Modulo constant and track historical parity counts
# STEP 2: The 'empty' prefix sum before index 0 is mathematically Even (0), so even_count starts at 1
# STEP 3: Iterate sequentially, maintaining a running prefix sum
# STEP 4: Based on the current sum's parity, add the opposite historical parity count to the answer
# STEP 5: Update the corresponding parity tracker for future iterations

class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        
        MOD = 10**9 + 7
        
        ans = 0
        current_sum = 0
        
        # Historical trackers
        even_count = 1                                               # Crucial base case: represents the implicit sum(0)
        odd_count = 0
        
        for num in arr:
            current_sum += num
            
            # Check the parity of the running prefix sum
            if current_sum % 2 == 1:
                # If current is Odd, it forms an odd subarray with all previous Even prefixes
                ans += even_count
                odd_count += 1
            else:
                # If current is Even, it forms an odd subarray with all previous Odd prefixes
                ans += odd_count
                even_count += 1
                
        # Return safely wrapped in the Modulo boundary
        return ans % MOD

"""
WHY EACH PART:
- even_count = 1: Without this, any odd subarray that starts exactly at index 0 would be missed because there would be no "previous even" to subtract from. 0 is an even number mathematically.
- ans += even_count (or odd_count): This dynamically calculates all valid combinations without ever looking backwards physically. It achieves O(1) combinatorics per step.
- current_sum % 2: Natively handles parity regardless of how large the running sum grows.

HOW IT WORKS (Example: arr = [2, 4]):
Init: even=1, odd=0, ans=0
num 2: sum=2 (Even). ans+=odd(0). even=2.
num 4: sum=6 (Even). ans+=odd(0). even=3.
Returns 0. (Correct, no odd numbers exist). ✓

KEY TECHNIQUE:
- Prefix Sums (State abstraction)
- Parity Math (Odd/Even characteristics)
- O(N) Dynamic Combinatorics

EDGE CASES:
- Array of purely even numbers: `odd_count` remains 0. Answer remains 0. ✓
- Extremely long arrays (size 10^5) of purely odd numbers: Alternates rapidly, accumulating massive combinations. The `ans % MOD` smoothly handles the gargantuan theoretical combinations. ✓

TIME COMPLEXITY: O(N) - We iterate through the array strictly once. Condition checks and arithmetic operations are purely O(1).
SPACE COMPLEXITY: O(1) - We allocate a few tracking variables (`ans`, `current_sum`, `odd_count`, `even_count`). No extra arrays or data structures are built, delivering a strict constant space profile.
"""

# 1248. Count Number of Nice Subarrays
# Difficulty: Medium
# https://leetcode.com/problems/count-number-of-nice-subarrays/

"""
PROBLEM:
Given an array of integers nums and an integer k. A continuous subarray is called nice 
if there are k odd numbers on it. Return the number of nice subarrays.

EXAMPLES:
Input: nums = [1,1,2,1,1], k = 3      → Output: 2
(The two nice subarrays are [1,1,2,1] and [1,2,1,1])

Input: nums = [2,4,6], k = 1          → Output: 0
(There are no odd numbers, so no subarray has 1 odd number)

Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2  → Output: 16
(Lots of combinations of evens around the two 1s)

CONSTRAINTS:
- 1 <= nums.length <= 50000
- 1 <= nums[i] <= 10^5
- 1 <= k <= nums.length

ALGORITHM LOGIC (Prefix Sum + Hash Map):
1. Transform the mental model: Evens are 0, Odds are 1.
2. The problem translates to: "Find the number of subarrays that sum to exactly k".
3. We keep a running total of odds seen so far (`curr_sum`).
4. At any point, if our current sum is X, and we want a subarray of sum k, we need to chop off a prefix of sum X - k.
5. We use a Hash Map (dictionary) to remember how many times we've seen each prefix sum in the past.

VISUALIZATION (nums = [1,1,2,1,1], k = 3):
Mental Array: [1, 1, 0, 1, 1]

Iter  | Num | IsOdd? | curr_sum | Look for (curr_sum - k) | Map before | Map After    | ans
---------------------------------------------------------------------------------------------
Init  |  -  |   -    |    0     |           -             | {0: 1}     | {0: 1}       |  0
  0   |  1  |   1    |    1     | 1 - 3 = -2 (Not in Map) | {0: 1}     | {0: 1, 1: 1} |  0
  1   |  1  |   1    |    2     | 2 - 3 = -1 (Not in Map) | {0: 1, 1: 1}| {0: 1, 1: 1, 2: 1} | 0
  2   |  2  |   0    |    2     | 2 - 3 = -1 (Not in Map) | (same)     | {0: 1, 1: 1, 2: 2} | 0
  3   |  1  |   1    |    3     | 3 - 3 =  0 (In Map: 1)  | (same)     | {... 3: 1}   |  1
  4   |  1  |   1    |    4     | 4 - 3 =  1 (In Map: 1)  | (same)     | {... 4: 1}   |  2

Total nice subarrays: 2 ✓
"""

# STEP 1: Initialize prefix_counts dictionary with {0: 1} to handle exact matches from index 0
# STEP 2: Initialize curr_sum and ans (total nice subarrays) to 0
# STEP 3: Iterate through every number in the array
# STEP 4: Add 1 to curr_sum if the number is odd
# STEP 5: Check if (curr_sum - k) exists in the dictionary, if so, add its count to ans
# STEP 6: Update the dictionary with the new curr_sum

class Solution:
    def numberOfSubarrays(self, nums: list[int], k: int) -> int:
        
        prefix_counts = {0: 1}                                         # Map to store frequency of prefix sums
        curr_sum = 0                                                   # Running sum of odd numbers
        ans = 0                                                        # Total count of valid subarrays
        
        for num in nums:                                               # Loop through each number
            
            if num % 2 != 0:                                           # If the number is odd (Binary Transformation)
                curr_sum += 1                                          
                
            target = curr_sum - k                                      # The prefix sum we need to chop off
            
            if target in prefix_counts:                                # If we've seen this sum before
                ans += prefix_counts[target]                           # Add its frequency to our answer
                
            if curr_sum in prefix_counts:                              # Update frequency of current sum
                prefix_counts[curr_sum] += 1
            else:
                prefix_counts[curr_sum] = 1
                
        return ans                                                     # Return final count

"""
WHY EACH PART:
- {0: 1}: This is the mathematical anchor. It means "we've seen a sum of 0 exactly once before starting". Without this, a valid subarray starting at index 0 wouldn't be counted because `curr_sum - k` would equal 0, but 0 wouldn't be in our map.
- num % 2 != 0: This is how we filter out even numbers. Even numbers don't add to `curr_sum`, but they DO trigger the dictionary check and update, effectively extending the length of valid subarrays.
- ans += prefix_counts[target]: Why += and not just + 1? Because if we saw the `target` sum 3 times in the past, it means there are 3 different starting points that lead to our current position. We must count all 3 valid subarrays.
- Dictionary update at the end: We must update the dictionary AFTER checking for the target. If we updated it before, we might accidentally use the current number to count a zero-length subarray (if k=0, though constraints say k>=1, it's best practice).

HOW IT WORKS (Example: nums = [2,2,2,1...], k = 1):
Index 0 (2): curr_sum = 0. Map becomes {0: 2}
Index 1 (2): curr_sum = 0. Map becomes {0: 3}
Index 2 (2): curr_sum = 0. Map becomes {0: 4}
Index 3 (1): curr_sum = 1. Target = 1 - 1 = 0. 
             Since '0' is in the map with a value of 4, we add 4 to our answer. 
             This correctly captures the 4 combinations:
             [2,2,2,1], [2,2,1], [2,1], and [1].

KEY TECHNIQUE:
- Prefix Sum + Hash Map: One of the most powerful patterns for "Subarray Sum Equals X" problems.
- State Tracking: Converting properties (odd/even) into countable states (1/0) allows arithmetic evaluation of arrays.

EDGE CASES:
- Only Evens ([2,4,6], k=1): `curr_sum` never increases, `target` is always negative, returns 0 ✓
- Exact Match from start ([1,1], k=2): Handles perfectly due to {0:1} initialization ✓
- Multiple Evens padded around odds: The dictionary accumulates the state without sum changing, multiplying the combinations naturally ✓

TIME COMPLEXITY: O(N) - We traverse the `nums` array exactly once. Dictionary lookups and insertions are O(1) on average.
SPACE COMPLEXITY: O(N) - In the worst case (e.g., all odd numbers), the dictionary will store up to N distinct prefix sums.

CONCEPTS USED:
- Prefix Sum Array
- Hash Map / Dictionary
- Two-Pointer abstraction (indirectly)
- Array transformation / Mapping
"""

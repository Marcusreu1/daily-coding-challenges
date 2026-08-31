# 1814. Count Nice Pairs in an Array
# Difficulty: Medium
# https://leetcode.com/problems/count-nice-pairs-in-an-array/

"""
PROBLEM:
You are given an array nums that consists of non-negative integers. 
Let us define rev(x) as the reverse of the non-negative integer x. For example, rev(123) = 321, and rev(120) = 21. 
A pair of indices (i, j) is nice if it satisfies all of the following conditions:
- 0 <= i < j < nums.length
- nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])
Return the number of nice pairs of indices. Since that number can be too large, return it modulo 10^9 + 7.

EXAMPLES:
Input: nums = [42,11,1,97] → Output: 2
Explanation: The two pairs are:
 - (0,3) : 42 + rev(97) = 42 + 79 = 121, 97 + rev(42) = 97 + 24 = 121.
 - (1,2) : 11 + rev(1) = 11 + 1 = 12, 1 + rev(11) = 1 + 11 = 12.

Input: nums = [13,10,35,24,76] → Output: 4

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^9

MATH RULES (ALGEBRAIC MANIPULATION & COMBINATORICS):
The given condition is:
nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])

By rearranging the terms to group indices together, we get:
nums[i] - rev(nums[i]) == nums[j] - rev(nums[j])

Let diff(x) = x - rev(x).
The condition simplifies to finding pairs (i, j) where diff(nums[i]) == diff(nums[j]).
Instead of O(N^2) brute force, we can process each number one by one. If we calculate a difference and we have already seen that exact difference 'k' times before, the current number can form 'k' new valid pairs. We add 'k' to our total pairs and then increment the count of this difference in a Hash Map.

VISUALIZATION (nums = [42, 11, 1, 97]):
Initial: freq_map = {}, nice_pairs = 0

i=0, num=42: rev(42)=24. diff = 42 - 24 = 18.
  - 18 is not in freq_map. 
  - freq_map = {18: 1}
  - nice_pairs = 0

i=1, num=11: rev(11)=11. diff = 11 - 11 = 0.
  - 0 is not in freq_map.
  - freq_map = {18: 1, 0: 1}
  - nice_pairs = 0

i=2, num=1: rev(1)=1. diff = 1 - 1 = 0.
  - 0 IS in freq_map (count = 1).
  - nice_pairs += 1 -> 1
  - freq_map = {18: 1, 0: 2}

i=3, num=97: rev(97)=79. diff = 97 - 79 = 18.
  - 18 IS in freq_map (count = 1).
  - nice_pairs += 1 -> 2
  - freq_map = {18: 2, 0: 2}

Result: 2 ✓
"""

from typing import List

# STEP 1: Initialize the modulo constant, a frequency dictionary, and a counter for the pairs.
# STEP 2: Iterate through every number in the array.
# STEP 3: Reverse the number using string slicing and calculate the difference: num - rev(num).
# STEP 4: If the difference exists in the dictionary, add its frequency to the pairs counter.
# STEP 5: Increment the frequency of this difference in the dictionary.
# STEP 6: Return the pairs counter modulo 10^9 + 7.

class Solution:
    def countNicePairs(self, nums: List[int]) -> int:
        
        MOD = 10**9 + 7
        freq_map = {}
        nice_pairs = 0
        
        for num in nums:
            
            # Fast string slicing to reverse the integer
            rev_num = int(str(num)[::-1])
            diff = num - rev_num
            
            # If we've seen this difference before, it forms new pairs with all previous occurrences
            if diff in freq_map:
                nice_pairs = (nice_pairs + freq_map[diff]) % MOD
                freq_map[diff] += 1
            else:
                # First time seeing this difference
                freq_map[diff] = 1
                
        return nice_pairs

"""
WHY EACH PART:
- int(str(num)[::-1]): Pythonic and heavily optimized way to reverse a number. Slicing [::-1] operates at the C-level.
- nice_pairs = (nice_pairs + freq_map[diff]) % MOD: Applies combinatorics dynamically. If 3 elements previously had the same difference, the 4th element forms 3 new pairs. We apply modulo instantly to avoid massive integers.
- freq_map[diff] += 1: Tracks the state in a Hash Map to achieve O(1) lookups per element.

KEY TECHNIQUE:
- Algebraic Simplification: Grouping elements by index to eliminate cross-dependency between i and j.
- Hash Map Frequency Counting: Transforming a combinatorics/pairing problem from O(N^2) to O(N) by caching previous states.

EDGE CASES:
- Palindromic numbers (e.g., 11, 1, 101): Difference will always be 0. Handled perfectly by the logic.
- Array with all identical elements: Will group entirely under a single dictionary key (diff 0), executing Gauss sum equivalent seamlessly.

TIME COMPLEXITY: O(N) - We iterate over the array exactly once. The string conversion and reversal take O(1) time because the maximum number constraint is 10^9 (at most 10 characters).
SPACE COMPLEXITY: O(N) - In the worst-case scenario (all elements yield unique differences), the Hash Map will store N key-value pairs.

CONCEPTS USED:
- Hash Maps (Dictionaries)
- Algebraic Equivalence
- Combinatorics
- String Manipulation
"""

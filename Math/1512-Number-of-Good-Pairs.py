# 1512. Number of Good Pairs
# Difficulty: Easy
# https://leetcode.com/problems/number-of-good-pairs/

"""
PROBLEM:
Given an array of integers `nums`, return the number of good pairs.
A pair (i, j) is called good if nums[i] == nums[j] and i < j.

EXAMPLES:
Input: nums = [1,2,3,1,1,3]
Output: 4
(Explanation: There are 4 good pairs: (0,3), (0,4), (3,4), (2,5) 0-indexed.)

Input: nums = [1,1,1,1]
Output: 6
(Explanation: Each pair in the array are good.)

Input: nums = [1,2,3]
Output: 0
(Explanation: No numbers are identical, so 0 pairs can be formed.)

CONSTRAINTS:
- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

ALGORITHM LOGIC (Hash Map & Progressive Combinatorics):
1. Instead of using a nested O(N^2) loop to check every possible pair, we can use a Hash Map (dictionary) to track frequencies in O(N) time.
2. We traverse the array exactly once from left to right.
3. Because we move left-to-right, any previously seen number naturally satisfies the `i < j` condition relative to our current position.
4. When we encounter a number `num`, it can form exactly one new pair with each of its previously seen identical twins. 
   Therefore, we add the historical frequency of `num` to our `total_pairs` accumulator.
5. After calculating the pairs, we increment the frequency of `num` in the Hash Map to make it available for future pairings.

VISUALIZATION (nums = [1, 2, 3, 1, 1]):
total = 0, counts = {}

num = 1: counts has no '1'. total = 0. counts updates to {1: 1}.
num = 2: counts has no '2'. total = 0. counts updates to {1: 1, 2: 1}.
num = 3: counts has no '3'. total = 0. counts updates to {1: 1, 2: 1, 3: 1}.
num = 1: counts HAS '1' (freq=1). total += 1 -> 1. counts updates to {..., 1: 2}.
num = 1: counts HAS '1' (freq=2). total += 2 -> 3. counts updates to {..., 1: 3}.

Loop finishes. Return total (3). ✓
"""

# STEP 1: Initialize the accumulator and the Hash Map for progressive counting
# STEP 2: Iterate linearly through the numbers
# STEP 3: If the number was seen before, it forms exactly 'N' new pairs, where 'N' is its previous count
# STEP 4: Register the current number's occurrence for future iterations
# STEP 5: Return the accumulated pairs

class Solution:
    def numIdenticalPairs(self, nums: list[int]) -> int:
        
        total_pairs = 0
        counts = {}
        
        for num in nums:
            
            # If the number exists, add its historical count to total_pairs
            if num in counts:
                total_pairs += counts[num]
                
            # Increment the current number's frequency
            counts[num] = counts.get(num, 0) + 1
            
        return total_pairs

"""
WHY EACH PART:
- counts = {}: The dictionary allows strictly O(1) lookup times. We don't rescan arrays.
- if num in counts:: This effectively isolates the combinatorial logic without relying on expensive factorial math (n*(n-1)/2).
- counts.get(num, 0) + 1: A safe way to increment a dictionary key in Python. If the key doesn't exist, it defaults to 0 and becomes 1.

HOW IT WORKS (Example: nums = [1, 1, 1]):
1st '1': total += 0. counts[1] = 1.
2nd '1': total += 1. counts[1] = 2.
3rd '1': total += 2. counts[1] = 3.
Final total: 0 + 1 + 2 = 3. (Pairs: (0,1), (0,2), (1,2)). ✓

KEY TECHNIQUE:
- Hash Map State Tracking
- Progressive Combinatorics
- Single Pass Optimization (O(N) iteration)

EDGE CASES:
- Array with all unique elements (e.g., [1, 2, 3]): The `if num in counts` block never triggers. Returns 0 correctly. ✓
- Array with all identical elements (e.g., [1, 1, 1, 1]): Accumulates as the sequence of triangular numbers (1 + 2 + 3 + 4...). Works flawlessly. ✓

TIME COMPLEXITY: O(N) - We iterate through the array of size N exactly once. Checking and updating the dictionary takes O(1) time on average.
SPACE COMPLEXITY: O(N) - In the worst case (all unique elements), we store N distinct keys in the dictionary.
"""

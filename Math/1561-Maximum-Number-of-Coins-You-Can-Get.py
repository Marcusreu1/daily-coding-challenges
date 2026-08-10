# 1561. Maximum Number of Coins You Can Get
# Difficulty: Medium
# https://leetcode.com/problems/maximum-number-of-coins-you-can-get/

"""
PROBLEM:
There are 3n piles of coins of varying size, you and your friends will take piles of coins as follows:
- In each step, you will choose any 3 piles of coins (not necessarily consecutive).
- Of your choice, Alice will pick the pile with the maximum number of coins.
- You will pick the next pile with the maximum number of coins.
- Bob will pick the last pile.
- Repeat until there are no more piles of coins.
Given an array of integers `piles` where piles[i] is the number of coins in the ith pile.
Return the maximum number of coins that you can have.

EXAMPLES:
Input: piles = [2,4,1,2,7,8]
Output: 9
(Explanation: Choose the triplet (2, 7, 8), Alice Pick the pile with 8 coins, you the pile with 7 coins and Bob the last one.
Choose the triplet (1, 2, 4), Alice Pick the pile with 4 coins, you the pile with 2 coins and Bob the last one.
The maximum number of coins which you can have are: 7 + 2 = 9.)

Input: piles = [2,4,5]
Output: 4

Input: piles = [9,8,7,6,5,1,2,3,4]
Output: 18
(Explanation: 
Sorted: [9,8,7,6,5,4,3,2,1]. 
Triplets: (9,8,1) -> I get 8. (7,6,2) -> I get 6. (5,4,3) -> I get 4. 
Total = 8 + 6 + 4 = 18.)

CONSTRAINTS:
- 3 <= piles.length <= 10^5
- piles.length % 3 == 0
- 1 <= piles[i] <= 10^4

ALGORITHM LOGIC (Greedy Sorting & Array Slicing):
1. To maximize our coins, we need to take the largest possible piles available.
2. Since Alice always takes the absolute largest in any triplet, the absolute best we can do is take the 2nd largest in the entire array.
3. We must not waste large piles on Bob. Therefore, we should force Bob to take the absolute smallest piles in the array.
4. By sorting the array in descending order, we can predictably extract our share.
5. In a descending array, Alice takes index 0, we take index 1, Bob takes the last index.
6. Then Alice takes index 2, we take index 3, Bob takes the second to last index.
7. We always get the odd indices (1, 3, 5, ...) up to exactly `2n` elements (since the remaining `n` elements at the tail are strictly for Bob).
8. We can achieve this extraction and summation in Python elegantly using list slicing.

VISUALIZATION (piles = [9, 8, 7, 6, 5, 1, 2, 3, 4]):
Sort Descending: [9, 8, 7, 6, 5, 4, 3, 2, 1]
n = 9 // 3 = 3 rounds.
Alice's boundary and our boundary ends at index 2*n = 6. (Bob takes the rest).

Valid bounds for us: Indices 1, 3, 5.
piles[1:6:2] extracts -> [8, 6, 4]
sum([8, 6, 4]) = 18. ✓
"""

# STEP 1: Sort the array descending to put the highest values at the front
# STEP 2: Calculate 'n' (the total number of rounds / number of coins we will take)
# STEP 3: Use slicing `[start:stop:step]` to extract only the 2nd best values mathematically
# STEP 4: Return the sum of the extracted slice

class Solution:
    def maxCoins(self, piles: list[int]) -> int:
        
        # Sort piles from highest to lowest
        piles.sort(reverse=True)
        
        # Calculate exactly how many coins each person gets
        n = len(piles) // 3
        
        # Extract our share: start at index 1, step by 2, and stop before Bob's trash section
        return sum(piles[1 : 2 * n : 2])

"""
WHY EACH PART:
- piles.sort(reverse=True): The greedy engine. Puts the most valuable coins right at the beginning so we can systematically grab them.
- 2 * n: Represents the mathematical cutoff. The first 2/3 of the array belongs strictly to Alice and Us. The last 1/3 belongs strictly to Bob. Stopping at `2 * n` ensures we don't accidentally grab Bob's small coins.
- piles[1 : 2*n : 2]: The Pythonic slice. `1` skips Alice's first coin. `:2` skips every subsequent coin Alice takes. It is written in C under the hood, making it significantly faster than writing a manual `for` loop in pure Python.

HOW IT WORKS (Example: piles = [2, 4, 5]):
Sorted desc: [5, 4, 2]
n = 3 // 3 = 1
Boundary = 2 * 1 = 2
Slice: piles[1 : 2 : 2] -> Extracts index 1 only -> [4]
sum([4]) = 4. ✓

KEY TECHNIQUE:
- Greedy Algorithm
- Sorting
- Array Slicing (Pythonic optimization)

EDGE CASES:
- Minimum array size (n=3): Correctly parses to exactly 1 extraction without index out-of-bounds errors. ✓
- Array with identical values (e.g., [2,2,2,2,2,2]): Sorts cleanly, returns the correct mechanical summation. ✓

TIME COMPLEXITY: O(N log N) - Where N is the length of the array. The dominant operation is the `sort()`. The slicing and summation execute in O(N) linear time.
SPACE COMPLEXITY: O(1) or O(N) - Sorting in Python (Timsort) takes O(N) space. The slice generates a temporary array of size N/3, scaling linearly with the input.
"""

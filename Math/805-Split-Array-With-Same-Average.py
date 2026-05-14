# 805. Split Array With Same Average
# Difficulty: Hard
# https://leetcode.com/problems/split-array-with-same-average/

"""
PROBLEM:
You are given an integer array nums.
You should move each element of nums into one of the two arrays A and B such that A and B are non-empty, 
and average(A) == average(B).
Return true if it is possible to achieve that and false otherwise.

EXAMPLES:
Input: nums = [1, 2, 3, 4, 5, 6, 7, 8]  → Output: True
Explanation: We can split the array into A = [1, 5, 5, 9] (Wait, input is 1 to 8).
Correct split for [1..8]: A = [1, 4, 5, 8] and B = [2, 3, 6, 7]. Both have an average of 4.5.

Input: nums = [3, 1]                    → Output: False
Explanation: Average of A will be 3.0, Average of B will be 1.0. Cannot be equal.

CONSTRAINTS:
- 1 <= nums.length <= 30
- 0 <= nums[i] <= 10^4

LOGIC RULES (MATH PRUNING & DP KNAPSACK):
1. If avg(A) == avg(B), then avg(A) == avg(Total).
2. Sum(A) / k = Sum(Total) / n  -->  Sum(A) = (Sum(Total) * k) / n.
3. Since Sum(A) must be an integer, (Sum(Total) * k) % n MUST strictly equal 0.
4. We only need to search for valid combinations of size 'k' up to n // 2. 
   If a valid smaller subset A exists, its complement B handles the other half automatically.
5. By pre-filtering impossible 'k' values, we prune the search tree exponentially.
6. Use DP (an array of sets) to record all achievable sums for every possible subset length 'i'.

VISUALIZATION (nums = [1, 2, 3, 4, 5, 6, 7, 8], sum = 36, n = 8):
Possible sizes for subset A (k): 1, 2, 3, 4.

Math Filter (Is (36 * k) % 8 == 0?):
- k = 1: 36 % 8 != 0  (Impossible to have avg 4.5 with 1 int)
- k = 2: 72 % 8 == 0  (Possible! Target sum for 2 elements = 72 / 8 = 9)
- k = 3: 108 % 8 != 0 (Impossible)
- k = 4: 144 % 8 == 0 (Possible! Target sum for 4 elements = 144 / 8 = 18)

DP checks size 2 for sum 9:
Finds (1 + 8) = 9. 
Returns True immediately! ✓
"""

# STEP 1: Calculate total sum and array length
# STEP 2: Pre-calculate if ANY subset length 'k' is mathematically possible. If not, return False early.
# STEP 3: Initialize DP array of sets. dp[i] will store all possible sums made from exactly 'i' elements.
# STEP 4: Populate the DP sets by iterating through each number and adding it to previous sums (backwards).
# STEP 5: Verify if the mathematically required target sum actually exists in our dp[k] set.

class Solution:
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        
        n = len(nums)
        total_sum = sum(nums)
        
        # Step 2: Math Pruning (The "WHERE" clause to filter out impossible tasks)
        is_possible = False
        for k in range(1, n // 2 + 1):
            if (total_sum * k) % n == 0:
                is_possible = True
                break
                
        if not is_possible:
            return False                                         # Pruned! No need to run expensive DP
            
        # Step 3: Initialize DP. dp[i] holds unique sums constructed with exactly 'i' numbers
        dp = [set() for _ in range(n // 2 + 1)]
        dp[0].add(0)                                             # 0 elements yield a sum of 0
        
        # Step 4: Populate DP sets
        for num in nums:
            # We iterate backwards to prevent reusing the current 'num' within the same pass
            for i in range(n // 2, 0, -1):
                for prev_sum in dp[i - 1]:
                    dp[i].add(prev_sum + num)
                    
        # Step 5: Final Validation
        for k in range(1, n // 2 + 1):
            if (total_sum * k) % n == 0:                         # If mathematically valid
                target_sum = (total_sum * k) // n
                if target_sum in dp[k]:                          # And physically achievable with our numbers
                    return True
                    
        return False

"""
WHY EACH PART:
- n // 2 + 1: We only evaluate subsets up to half the total array length because if subset A is larger 
  than half, subset B must be smaller than half. It is perfectly symmetric.
- backwards loop (range(n // 2, 0, -1)): Crucial 1D-DP pattern. If we went forward, a single number 
  could theoretically be added multiple times into larger length sets. 
- dp[i-1]: We only add the current number to sums that were successfully built using strictly one element less.
- target_sum in dp[k]: Python set lookup is O(1). This makes the final validation instantaneous.

HOW IT WORKS (Example: nums=[3, 1], sum=4, n=2):

Math Filter:
├── k = 1 (half of n). 
├── (4 * 1) % 2 == 0? Yes. Target = 2. 
└── is_possible = True.

DP Execution:
Initial: dp[0]={0}, dp[1]={}
Num = 3:
├── i=1: dp[0] has 0 -> dp[1].add(0 + 3). dp[1] = {3}
Num = 1:
├── i=1: dp[0] has 0 -> dp[1].add(0 + 1). dp[1] = {1, 3}

Final Validation:
├── k = 1: target_sum is 2. 
├── Is 2 in dp[1] ({1, 3})? No.
└── Return False. ✓

EDGE CASES:
- Array length 1: Loop n//2 becomes range(1, 0), is_possible stays False. Returns False instantly. ✓
- All identical elements ([2, 2, 2, 2]): Math immediately approves k=1. DP instantly builds {2}. Returns True. ✓
- Sum equals 0: Handled flawlessly. (0 * k) % n is always 0. target is 0.

TIME COMPLEXITY: O(N * (N/2) * 2^(N/2)) in extreme theoretical worst case without bound constraints, 
but practically O(N^2 * max_sum). Given N <= 30 and sum <= 300,000, the DP limits computations efficiently.
Overall runtime usually stays within milliseconds.

SPACE COMPLEXITY: O(N * max_sum/2)
The DP array contains N/2 sets. In the worst case, these sets store distinct reachable sums.
Memory is heavily constrained by the problem limits and Python's efficient set implementation.
"""

# 2240. Number of Ways to Buy Pens and Pencils
# Difficulty: Medium
# https://leetcode.com/problems/number-of-ways-to-buy-pens-and-pencils/

"""
PROBLEM:
You are given an integer total indicating the amount of money you have. You are also given two integers cost1 and cost2 indicating the price of a pen and pencil respectively. You can spend part or all of your money to buy multiple quantities (or none) of each kind of writing utensil.
Return the number of distinct ways you can buy some number of pens and pencils.

EXAMPLES:
Input: total = 20, cost1 = 10, cost2 = 5 → Output: 9
Explanation: The price of a pen is 10 and the price of a pencil is 5.
- If you buy 0 pens, you have 20 left. You can buy 0, 1, 2, 3, or 4 pencils (5 ways).
- If you buy 1 pen, you have 10 left. You can buy 0, 1, or 2 pencils (3 ways).
- If you buy 2 pens, you have 0 left. You can buy 0 pencils (1 way).
Total ways = 5 + 3 + 1 = 9.

Input: total = 5, cost1 = 10, cost2 = 10 → Output: 1
Explanation: You cannot afford to buy any pen or pencil, so you can only buy 0 pens and 0 pencils (1 way).

CONSTRAINTS:
- 1 <= total, cost1, cost2 <= 10^6

MATH RULES (LINEAR DIOPHANTINE INEQUALITIES & LOOP MINIMIZATION):
We are solving for combinations of (x, y) such that: x * cost1 + y * cost2 <= total.
Instead of an O(N^2) brute-force nested loop, we iterate exclusively over one variable (x).
For any fixed quantity of item 1 (x), the remaining budget is R = total - (x * cost1).
The exact number of item 2 (y) combinations we can form with R is strictly (R // cost2) + 1 (the +1 accounts for buying 0 of item 2).
To optimize execution speed, we always iterate over the MORE EXPENSIVE item. 
Iterating over an item that costs 1000 takes far fewer steps than iterating over an item that costs 1.
"""

# STEP 1: Swap costs if necessary so that cost1 is always the more expensive item.
# STEP 2: Initialize the ways counter.
# STEP 3: Iterate over every possible quantity of the expensive item we can buy.
# STEP 4: Mathematically calculate how many combinations of the cheaper item can be bought with the leftover money.
# STEP 5: Add to total ways and return.

class Solution:
    def waysToBuyPensPencils(self, total: int, cost1: int, cost2: int) -> int:
        
        # Optimization: Guarantee cost1 is the larger denomination to minimize loop iterations
        if cost1 < cost2:
            cost1, cost2 = cost2, cost1
            
        ways = 0
        
        # Iterate over the maximum possible number of expensive items we can afford
        max_expensive_items = total // cost1
        
        for count in range(max_expensive_items + 1):
            
            # Money left after buying 'count' expensive items
            remaining_budget = total - (count * cost1)
            
            # The number of valid options for the cheaper item is the division + 1 (to include 0 items)
            ways += (remaining_budget // cost2) + 1
            
        return ways

"""
WHY EACH PART:
- cost1, cost2 = cost2, cost1: Reduces loop size drastically. If total=10^6, cost1=1, cost2=10^5, swapping drops iterations from 1,000,000 to just 10.
- remaining_budget // cost2 + 1: Solves for the secondary variable in O(1) mathematical time per iteration, completely eliminating the need for a nested loop.

KEY TECHNIQUE:
- Bounded Search Optimization: Fixing one axis of a 2D constraint and calculating the other algebraically.
- Execution Pruning: Deliberately choosing the axis with the smallest search space (the most expensive item).

EDGE CASES:
- Items are strictly more expensive than the total budget (e.g., total = 5, cost1 = 10, cost2 = 10): `max_expensive_items` is 0. Loop runs exactly once. `remaining_budget = 5`. `5 // 10 + 1 = 1`. Returns 1. Correct!
- Exact multiples (e.g., total = 10, cost1 = 5): Remainder drops perfectly to 0, adding exactly 1 option at the end.

TIME COMPLEXITY: O(total / max(cost1, cost2)) - The loop runs proportionally to how many of the expensive items fit into the total budget. This is exceptionally fast.
SPACE COMPLEXITY: O(1) - Only a few scalar integer variables are allocated in memory.
"""

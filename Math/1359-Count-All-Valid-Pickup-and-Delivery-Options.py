# 1359. Count All Valid Pickup and Delivery Options
# Difficulty: Hard
# https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/

"""
PROBLEM:
Given n orders, each order consists of a pickup services (P_i) and a delivery service (D_i).
Count all valid pickup/delivery possible sequences such that delivery(i) is always after pickup(i).
Since the answer may be too large, return it modulo 10^9 + 7.

EXAMPLES:
Input: n = 1
Output: 1
(Explanation: Unique direction is [P1, D1])

Input: n = 2
Output: 6
(Explanation: All possible 6 sequences are:
(P1,P2,D1,D2), (P1,P2,D2,D1), (P1,D1,P2,D2), (P2,P1,D1,D2), (P2,P1,D2,D1), (P2,D2,P1,D1)
An invalid sequence like (P1,D2,P2,D1) is dropped because D2 is performed before P2.)

Input: n = 3
Output: 90

CONSTRAINTS:
- 1 <= n <= 500

ALGORITHM LOGIC (Permutation & Dynamic Programming):
1. Let's build the solution inductively. Suppose we already know the valid sequences for (n - 1) orders.
2. For (n - 1) orders, the total number of elements currently placed in a sequence is 2 * (n - 1).
3. The number of slots (spaces between elements, including ends) available to insert a new element is:
   Slots = 2 * (n - 1) + 1 = 2n - 1
4. We need to insert both P_n and D_n into these slots such that P_n comes before D_n.
   - Case 1: Both P_n and D_n are placed in the exact same slot (as "P_n D_n"). There are (2n - 1) choices.
   - Case 2: P_n and D_n are placed in two different slots. We choose 2 distinct slots out of (2n - 1).
     Formula: Combinations(2n - 1, 2) = ((2n - 1) * (2n - 2)) / 2 = (2n - 1) * (n - 1)
5. Total choices for adding the n-th order = (2n - 1) + (2n - 1) * (n - 1) 
                                           = (2n - 1) * (1 + n - 1) 
                                           = (2n - 1) * n
6. Therefore: Ans(n) = Ans(n - 1) * (2n - 1) * n

VISUALIZATION (n = 2):
For n = 1, sequence is [P1, D1]. Total elements = 2. Ans = 1.

Now adding the 2nd order (P2, D2):
Available elements = 2. Slots available = 2 + 1 = 3 slots.
Slots look like:  ^ P1 ^ D1 ^
Choices to place P2 and D2 = (2 * 2 - 1) * 2 = 3 * 2 = 6 choices.
New Total Ans = 1 * 6 = 6. ✓
"""

# STEP 1: Define the modulo constant (10^9 + 7)
# STEP 2: Initialize the base case answer for n=1 to 1
# STEP 3: Loop from 2 up to n (inclusive) to process each subsequent order
# STEP 4: In each step, multiply the accumulated answer by the new choices: (2 * i - 1) * i
# STEP 5: Apply the modulo constraint to keep integer growth safe
# STEP 6: Return the final answer

class Solution:
    def countOrders(self, n: int) -> int:
        
        mod_val = 10**9 + 7                                          # Strict modulo requirement
        ans = 1                                                      # Base Case: 1 order = 1 valid sequence
        
        for i in range(2, n + 1):                                    # Inductively calculate up to n
            
            # Multiply by permutations of the current step: slots * current index
            ans = ans * (2 * i - 1) * i
            
            # Apply modulo at each loop iteration to prevent integer overflow or slowing down memory
            ans %= mod_val
            
        return ans

"""
WHY EACH PART:
- ans = 1: The calculation scales multiplicatively. Starting at 1 ensures the chain reaction of the product works perfectly.
- (2 * i - 1) * i: This is the simplified algebraic equation of the combined slot insertion logic. It calculates the exact combinations added by the new pair in constant time.
- ans %= mod_val: Placed inside the loop rather than only at the final return. In Python, integers have arbitrary precision and can grow infinitely, but doing operations on giant numbers is slow. Keeping `ans` small ensures O(1) step operations.

HOW IT WORKS (Example: n = 3):
- Loop i = 2: ans = 1 * (3) * 2 = 6. ans % MOD = 6.
- Loop i = 3: ans = 6 * (5) * 3 = 6 * 15 = 90. ans % MOD = 90.
Returns 90. ✓

KEY TECHNIQUE:
- Combinatorics Optimization
- Dynamic Programming (Space-Optimized to O(1) variables)
- Aarithmetic Modular Management

EDGE CASES:
- n = 1: The loop `range(2, 2)` does not execute. Returns the initial `ans = 1`. ✓
- Maximum constraint (n = 500): The single loop runs 500 times. Thanks to the internal modulo, the operation executes instantly in a fraction of a millisecond. ✓

TIME COMPLEXITY: O(N) - We run a single linear loop from 2 to N. Every arithmetic step inside is O(1).
SPACE COMPLEXITY: O(1) - We only use two integer storage allocations (`mod_val` and `ans`), independent of the size of N.

CONCEPTS USED:
- Permutations & Combinations
- Modular Arithmetic
- Dynamic Programming
"""

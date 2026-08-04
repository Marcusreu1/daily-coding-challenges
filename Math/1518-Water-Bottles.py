# 1518. Water Bottles
# Difficulty: Easy
# https://leetcode.com/problems/water-bottles/

"""
PROBLEM:
There are `numBottles` water bottles that are initially full of water. You can exchange 
`numExchange` empty water bottles from the market with one full water bottle.
The operation of drinking a full water bottle turns it into an empty bottle.
Given the two integers `numBottles` and `numExchange`, return the maximum number of water 
bottles you can drink.

EXAMPLES:
Input: numBottles = 9, numExchange = 3
Output: 13
(Explanation: You can exchange 3 empty bottles to get 1 full water bottle.
Number of water bottles you can drink: 9 + 3 + 1 = 13.)

Input: numBottles = 15, numExchange = 4
Output: 19
(Explanation: You can exchange 4 empty bottles to get 1 full water bottle. 
Number of water bottles you can drink: 15 + 3 + 1 = 19.)

CONSTRAINTS:
- 1 <= numBottles <= 100
- 2 <= numExchange <= 100

ALGORITHM LOGIC (O(1) Mathematical Abstraction):
1. The standard approach is simulating the process with a `while` loop. However, this can be 
   solved instantly using O(1) mathematics by analyzing the "net cost" of an exchange.
2. When you exchange `E` empty bottles, you get 1 full bottle. After drinking it, you are left 
   with 1 empty bottle. 
3. Therefore, the net loss of empty bottles for every new drink is strictly `E - 1`.
4. How many extra drinks can you get? You divide your starting bottles by this net cost: `(E - 1)`.
5. But there's a strict physical limitation: you must have at least `E` bottles to perform a trade, 
   you cannot pay the "net cost" on the last transaction. 
6. To mathematically offset this rule, we simply subtract 1 from our initial `numBottles` pool 
   before dividing. The exact number of bonus drinks becomes: (numBottles - 1) // (numExchange - 1).
7. The total is just the initial bottles plus the bonus drinks.

VISUALIZATION (numBottles = 15, numExchange = 4):
Base drinks = 15
Net cost per trade = (4 - 1) = 3 empty bottles per new drink.
Adjusted pool for trading = (15 - 1) = 14.

Extra drinks = 14 // 3 = 4.
Total drinks = 15 + 4 = 19. ✓
"""

# STEP 1: Return the mathematical derivation directly without simulating the exchanges.

class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        
        # Calculate extra bottles using the Net Exchange Rate formula
        # Total = Initial + Extra
        return numBottles + (numBottles - 1) // (numExchange - 1)

"""
WHY EACH PART:
- (numExchange - 1): Represents the mathematical net loss. Giving away X bottles but getting 1 back means you actually only "spent" X-1 bottles to get a drink.
- (numBottles - 1): Prevents the formula from granting a trade when you have exactly the net cost left but not the physical upfront cost. For example, if you have 3 bottles and need 4 to trade, (3) // (4-1) would give 1 (wrong), but (3-1) // (4-1) gives 0 (correct).
- // : Floor division natively handles integer truncation in Python.

HOW IT WORKS (Example: numBottles = 2, numExchange = 3):
Formula: 2 + (2 - 1) // (3 - 1)
2 + 1 // 2
2 + 0
Result: 2. (Correct, because we don't have enough to make the 3-bottle exchange). ✓

KEY TECHNIQUE:
- Mathematical Abstraction (Net Cost Derivation)
- O(1) Constant Time Evaluation

EDGE CASES:
- numBottles is exactly 1 less than numExchange (e.g., 2 and 3). Formula natively evaluates the bonus component to 0. ✓
- numExchange is minimum constraint (2): Denominator becomes (2-1) = 1. Divides smoothly without zero-division error. ✓

TIME COMPLEXITY: O(1) - Pure arithmetic evaluation. This is infinitely more scalable than the standard O(log_E(N)) simulation approach, completing in effectively 1 CPU cycle.
SPACE COMPLEXITY: O(1) - Zero memory allocated, entirely evaluated in the return stream.
"""

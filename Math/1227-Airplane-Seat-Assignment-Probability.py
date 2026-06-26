# 1227. Airplane Seat Assignment Probability
# Difficulty: Medium
# https://leetcode.com/problems/airplane-seat-assignment-probability/

"""
PROBLEM:
`n` passengers board an airplane with exactly `n` seats. The first passenger has lost 
the ticket and picks a seat randomly. But after that, the rest of the passengers will:
- Take their own seat if it is still available, and
- Pick other seats randomly when they find their seat occupied

Return the probability that the nth person gets his own seat.

EXAMPLES:
Input: n = 1
Output: 1.00000
Explanation: The first person can only get the first seat.

Input: n = 2
Output: 0.50000
Explanation: The second person has a probability of 0.5 to get the second seat (when first person gets the first seat).

CONSTRAINTS:
- 1 <= n <= 10^5

MATHEMATICAL INTUITION (THE "TRICK"):
This is a famous probability brain-teaser. 
The naive approach is to try and simulate the probabilities using Dynamic Programming, 
which gets incredibly complicated. 

Instead, look at the symmetry of the problem.
The chain of passengers picking random seats only STOPS when someone randomly picks:
1. Seat 1 (The first passenger's actual seat) -> The chain breaks, everyone else gets their correct seat, including passenger `n`.
2. Seat `n` (The last passenger's actual seat) -> Passenger `n` is doomed and will not get their seat.

If a displaced passenger picks any other seat `k`, the problem just delegates to passenger `k`, 
and the chain continues. 

At EVERY step where a passenger is forced to pick a random seat, BOTH Seat 1 and Seat `n` 
are still available. Because they are always both available in the pool of remaining choices, 
the probability of picking Seat 1 is EXACTLY equal to the probability of picking Seat `n`.

It is a perfectly symmetric coin flip. 
Thus, for any n > 1, the probability is always 50% (0.5).
"""

# STEP 1: If there is only 1 passenger, they mathematically must get their seat (1.0).
# STEP 2: For any other number of passengers, the symmetry dictates a 0.5 probability.
# STEP 3: Return the result in O(1) time.

class Solution:
    def nthPersonGetsNthSeat(self, n: int) -> float:
        
        # If there's only 1 seat, the probability is 100%
        if n == 1:
            return 1.0
            
        # For any n > 1, the probability is a 50/50 coin flip
        return 0.5

"""
WHY EACH PART:
- n == 1: The only edge case where the symmetry doesn't apply because Seat 1 AND Seat `n` are the exact same seat.
- return 0.5: Mathematical proof through symmetry. No simulation loops required.

HOW IT WORKS (Example: n = 3):
Passenger 1 has 3 choices:
1. Picks Seat 1 (1/3 prob): Passenger 2 gets Seat 2, Passenger 3 gets Seat 3. (WIN)
2. Picks Seat 3 (1/3 prob): Passenger 2 gets Seat 2, Passenger 3 gets Seat 1. (LOSE)
3. Picks Seat 2 (1/3 prob): Passenger 2 is now displaced. 
   Passenger 2 must pick randomly between Seat 1 and Seat 3.
   - Picks Seat 1 (1/2 prob): Passenger 3 gets Seat 3. (WIN)
   - Picks Seat 3 (1/2 prob): Passenger 3 gets Seat 1. (LOSE)

Total Probability of WIN:
= Prob(P1 picks S1) + Prob(P1 picks S2) * Prob(P2 picks S1)
= (1/3) + (1/3) * (1/2)
= (1/3) + (1/6)
= 3/6 = 0.5 ✓

TIME COMPLEXITY: O(1) - Constant time. No loops or recursion.
SPACE COMPLEXITY: O(1) - Constant space. 

CONCEPTS USED:
- Probability Theory
- Mathematical Induction / Symmetry
- Brain Teaser / Logic Puzzle
"""

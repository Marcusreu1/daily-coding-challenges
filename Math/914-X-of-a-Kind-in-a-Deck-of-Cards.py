# 914. X of a Kind in a Deck of Cards
# Difficulty: Easy
# https://leetcode.com/problems/x-of-a-kind-in-a-deck-of-cards/

"""
PROBLEM:
You are given an integer array `deck` where each integer represents the number on a card.
Partition the cards into one or more groups such that:
1. Each group has exactly X cards.
2. All the cards in each group have the same integer.
3. X >= 2.
Return true if and only if such a partition is possible.

EXAMPLES:
Input: deck = [1,2,3,4,4,3,2,1]
Output: true (Partition into [1,1], [2,2], [3,3], [4,4]. X = 2)

Input: deck = [1,1,1,2,2,2,3,3]
Output: false (Counts are 3, 3, and 2. No common X >= 2 divides all of them).

Input: deck = [1]
Output: false (Not enough cards to form a group of X >= 2).

CONSTRAINTS:
- 1 <= deck.length <= 10^4
- 0 <= deck[i] < 10^4

MATHEMATICAL REDUCTION:
Instead of simulating the grouping, we just need to look at the frequencies of each card.
If card A appears 4 times, and card B appears 6 times, we need an X that divides both 4 and 6 perfectly.
The Greatest Common Divisor (GCD) is the mathematical tool for this.
If the GCD of all frequencies in the deck is >= 2, the partition is possible. If it's 1, it's impossible.

VISUALIZATION (deck = [1,1,1,1,2,2,2,2,2,2]):
Count frequencies:
Card '1' -> 4 times
Card '2' -> 6 times

Calculate GCD of (4, 6):
Divisors of 4: 1, 2, 4
Divisors of 6: 1, 2, 3, 6
Greatest Common Divisor = 2

Since GCD (2) >= 2, we return True. We can make groups of 2.
"""

from collections import Counter
import math

# STEP 1: Count the frequency of each unique card in the deck
# STEP 2: Extract just the frequency values (we no longer care about the card IDs)
# STEP 3: Iterate through the frequencies and calculate the running GCD
# STEP 4: Check if the final GCD is strictly greater than or equal to 2

class Solution:
    def hasGroupsSizeX(self, deck: list[int]) -> bool:
        
        counts = Counter(deck)                                                 # Dictionary of {card: frequency}
        frequencies = list(counts.values())                                    # List of just the frequencies
        
        current_gcd = frequencies[0]                                           # Initialize GCD with the first frequency
        
        for f in frequencies[1:]:                                              # Loop through the remaining frequencies
            current_gcd = math.gcd(current_gcd, f)                             # Update running GCD
            
        return current_gcd >= 2                                                # True if GCD is valid (>= 2)

"""
WHY EACH PART:
- Counter(deck): Efficiently tallies up occurrences in O(N) time.
- list(counts.values()): We only care about the quantities, not what number is on the card itself.
- math.gcd(): Python's built-in Greatest Common Divisor function. It safely handles the math without needing a custom Euclidean algorithm.
- for f in frequencies[1:]: The GCD of a list of numbers is calculated by successively applying GCD. GCD(a, b, c) = GCD(GCD(a, b), c).

HOW IT WORKS (Example: [1,1,1,1,2,2,2,2,2,2,3,3]):

Initial State:
├── counts = {1: 4, 2: 6, 3: 2}
├── frequencies = [4, 6, 2]
├── current_gcd = 4

Iteration 1 (f = 6):
├── math.gcd(4, 6) = 2
└── current_gcd = 2

Iteration 2 (f = 2):
├── math.gcd(2, 2) = 2
└── current_gcd = 2

Final Check:
└── return 2 >= 2  -> True ✓

KEY TECHNIQUE:
- Frequency Counting + Greatest Common Divisor (GCD). By abstracting the physical cards into mathematical counts, the problem shrinks from a complex array-partitioning task into a simple math reduction.

EDGE CASES:
- Deck length is 1 (e.g., [1]): Frequency is 1. GCD is 1. 1 >= 2 is False. ✓
- All cards are the same (e.g., [1,1,1,1]): Frequency is [4]. Loop doesn't run. current_gcd is 4. 4 >= 2 is True. ✓
- Large prime frequencies (e.g., [1,1,1, 2,2,2]): Frequencies [3, 3]. GCD is 3. True. ✓

TIME COMPLEXITY: O(N) - N to count frequencies using Counter, plus O(K) for GCD calculation where K is the number of unique cards. Since K <= N, total is O(N).
SPACE COMPLEXITY: O(K) - Storing the Counter dictionary and frequency list requires memory proportional to the number of unique cards K.

CONCEPTS USED:
- Hash Map / Counting
- Number Theory (Greatest Common Divisor)
"""

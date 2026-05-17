# 810. Chalkboard XOR Game
# Difficulty: Hard
# https://leetcode.com/problems/chalkboard-xor-game/

"""
PROBLEM:
Alice and Bob take turns playing a game, with Alice starting first.
Initially, there are n integers on a chalkboard. 
In each player's turn, that player makes a move consisting of erasing exactly one integer.
If the bitwise XOR of all the elements on the board evaluates to 0, then the player whose turn it is wins.
(Also, if the board evaluates to 0 initially, Alice wins).
If a player erases an element and the XOR of the remaining elements becomes 0, they lose.
Return true if and only if Alice wins the game, assuming both players play optimally.

EXAMPLES:
Input: nums = [1, 1, 2]   → Output: False
Explanation: 
- Alice has two choices: erase 1 or erase 2.
- If she erases 1, the board becomes [1, 2]. XOR is 1 ^ 2 = 3. 
  Bob then erases 2, board is [1]. XOR is 1. Alice's turn, she erases 1. Board is [], XOR is 0. Bob wins.
- If she erases 2, board becomes [1, 1]. XOR is 1 ^ 1 = 0. Alice immediately loses because she handed Bob a 0.
Conclusion: Bob wins.

Input: nums = [0, 1]      → Output: True
Explanation: Length is even. Alice can always win.

CONSTRAINTS:
- 1 <= nums.length <= 1000
- 0 <= nums[i] < 2^16

LOGIC RULES (GAME THEORY & XOR PARITY):
1. A player wins immediately if the board's XOR sum is 0 at the start of their turn.
2. A player faces a "losing state" ONLY if erasing ANY element makes the remaining XOR 0.
3. Mathematically: Total XOR = S. Erasing element x leaves S ^ x. 
   If S ^ x == 0 for all x, then x must equal S for all elements.
4. If all elements equal S, and there is an EVEN number of elements, the Total XOR (S ^ S ^ S...) would be 0.
   But we assumed the player hasn't won yet, so S != 0. This is a mathematical contradiction.
5. Conclusion: It is IMPOSSIBLE to be trapped in a losing state if the board has an EVEN number of elements.
6. Since Alice starts, if length is EVEN, she will never lose. Bob will always receive an ODD length and eventually lose.

VISUALIZATION (nums = [1, 2, 3]):
- Initial XOR: 1 ^ 2 ^ 3 = 0.
- Is initial XOR == 0? YES.
- Alice wins immediately before even making a move. Return True. ✓

VISUALIZATION (nums = [1, 1, 2]):
- Initial XOR: 1 ^ 1 ^ 2 = 2. (Not 0)
- Length of nums: 3 (ODD).
- Can Alice survive? Since it's odd, she might be trapped. And she is. Return False. ✓
"""

# STEP 1: Calculate the total XOR of the array to check for an immediate win
# STEP 2: Use Python's built-in reduce to apply XOR cumulatively across the list
# STEP 3: Return True if the total XOR is 0, OR if the length of the array is even

from functools import reduce
import operator

class Solution:
    def xorGame(self, nums: list[int]) -> bool:
        
        # Step 1 & 2: Calculate the XOR sum of all elements
        xor_sum = reduce(operator.xor, nums)
        
        # Step 3: Game Theory deduction
        # Alice wins if XOR is 0 initially, or if she starts with an even number of elements
        return xor_sum == 0 or len(nums) % 2 == 0

"""
WHY EACH PART:
- reduce(operator.xor, nums): The fastest and most Pythonic way to apply the ^ operator across an entire array. 
  It essentially does nums[0] ^ nums[1] ^ nums[2]... natively in C.
- xor_sum == 0: Checks Rule 1 of the game. If the board evaluates to 0 initially, Alice wins without playing.
- len(nums) % 2 == 0: Checks the parity. Because an even length mathematically guarantees at least one safe move, 
  Alice can just pass the "trap" to Bob forever until the game ends.

HOW IT WORKS (Example dry run for nums = [1, 2, 3, 4]):

Initial state:
├── Length: 4 (Even)
├── xor_sum: 1 ^ 2 ^ 3 ^ 4 = 4.
├── Is xor_sum == 0? False.
├── Is length % 2 == 0? True.
└── Returns True. ✓

Alice knows she just has to pick an element that doesn't make the XOR 0. 
Since length is 4 (Even), we mathematically proved that at least one such element MUST exist. 
She picks it. Bob gets 3 elements (Odd). He might be forced to make it 0. Alice wins.

EDGE CASES:
- Empty array? Constraints say 1 <= nums.length. 
- All identical elements even length (e.g., [5, 5, 5, 5]): XOR sum is 0. Alice wins immediately.
- All identical elements odd length (e.g., [5, 5, 5]): XOR sum is 5. Length is 3. Alice is forced to pick 5. 
  Remaining board is [5, 5] with XOR 0. Alice loses. Returns False properly. ✓

TIME COMPLEXITY: O(N)
Where N is the length of `nums`. The `reduce` function iterates through the array exactly once to compute the XOR sum.
Evaluating the length and boolean condition is O(1). Overall time is strictly O(N).

SPACE COMPLEXITY: O(1)
We only store the scalar result of the XOR sum (`xor_sum`). No additional data structures are created. Memory usage is constant.
"""

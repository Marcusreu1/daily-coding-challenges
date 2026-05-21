# 837. New 21 Game
# Difficulty: Medium
# https://leetcode.com/problems/new-21-game/

"""
PROBLEM:
Alice plays the following game, loosely based on the card game "21".
Alice starts with 0 points and draws numbers while she has less than k points.
During each draw, she gains an integer number of points randomly from the range [1, w], where each integer 
is drawn with equal probability. Alice stops drawing numbers when she gets k or more points.
Return the probability that Alice has n or fewer points.

EXAMPLES:
Input: n = 10, k = 1, w = 10    → Output: 1.00000
Explanation: Alice gets a single card, then stops. Her points are between 1 and 10. All outcomes are <= 10.

Input: n = 21, k = 17, w = 10   → Output: 0.73278

CONSTRAINTS:
- 0 <= k <= n <= 10^4
- 1 <= w <= 10^4
- Answers within 10^-5 of the actual answer are considered correct.

LOGIC RULES (DYNAMIC PROGRAMMING & SLIDING WINDOW):
1. Let dp[i] be the probability of getting exactly i points.
2. To reach exactly i points, Alice must have been at a score 'j' (where i - w <= j <= i - 1) and drawn the card (i - j).
3. Since Alice STOPS when reaching k, she can only draw from states where j < k.
4. dp[i] = Sum of valid dp[j] / w.
5. Instead of recalculating the sum of the last 'w' probabilities for every 'i' (which takes O(N*W) time), 
   we maintain a running `window_sum`. This reduces the time complexity to O(N).
6. The maximum points Alice can get is (k - 1) + w. If n is greater than or equal to this, success is guaranteed.

VISUALIZATION (n = 21, k = 17, w = 10):
dp[0] = 1.0
window_sum starts at 1.0.

For i = 1:
- dp[1] = window_sum / 10 = 1.0 / 10 = 0.1
- Since 1 < 17, Alice can draw from here. window_sum += dp[1] (window_sum becomes 1.1)

For i = 2:
- dp[2] = window_sum / 10 = 1.1 / 10 = 0.11
- Since 2 < 17, window_sum += dp[2] (window_sum becomes 1.21)

This continues. Once i >= 17 (e.g., i = 17):
- dp[17] = window_sum / 10. 
- Since 17 >= 17, Alice STOPS. This probability is added to our final answer. 
- It is NOT added to window_sum because she can't draw from 17.
"""

# STEP 1: Handle mathematically guaranteed edge cases (100% win rate)
# STEP 2: Initialize DP array and the running window sum
# STEP 3: Iterate through all possible scores up to 'n'
# STEP 4: Calculate the probability of reaching score 'i'
# STEP 5: Add to window_sum if the game can continue, else add to final result if the game stops
# STEP 6: Slide the window by removing probabilities that are now out of 'w' range

class Solution:
    def new21Game(self, n: int, k: int, w: int) -> float:
        
        # Step 1: Edge Cases. 
        # If k is 0, she never draws, ends at 0 <= n.
        # If n is higher than the max possible score (k - 1 + w), she can never bust.
        if k == 0 or n >= k + w - 1:
            return 1.0
            
        dp = [0.0] * (n + 1)
        dp[0] = 1.0
        
        window_sum = 1.0
        result_probability = 0.0
        
        # Step 3: Fill DP up to n
        for i in range(1, n + 1):
            
            # Step 4: The chance of reaching 'i' is the sum of valid previous states divided by 'w'
            dp[i] = window_sum / w
            
            # Step 5: Route the probability
            if i < k:
                window_sum += dp[i]               # Alice can keep drawing, add state to window
            else:
                result_probability += dp[i]       # Alice stops. Since i <= n, this is a winning final state
                
            # Step 6: Slide the window. 
            # We subtract the probability of the state that is exactly 'w' steps behind us.
            # But ONLY if it was actually part of the window_sum (meaning it was < k).
            if i - w >= 0 and i - w < k:
                window_sum -= dp[i - w]
                
        return result_probability

"""
WHY EACH PART:
- n >= k + w - 1: The absolute maximum score is when Alice is at k - 1 points and draws the highest card w. 
  If n covers this, calculating DP is a waste of time.
- dp[i] = window_sum / w: Since there are 'w' cards, each valid previous state has a (1/w) chance of reaching 'i'.
- i < k route: We only accumulate window_sum from states where Alice is ALLOWED to draw a card.
- i - w < k check: If a state was >= k, it was never added to window_sum (routed to result_probability instead). 
  Therefore, we shouldn't subtract it when the window slides past it.

HOW IT WORKS (Example dry run for n = 2, k = 1, w = 2):
Edge case: max score is (1 - 1) + 2 = 2. n is 2. 2 >= 2. Returns 1.0 immediately!

Let's do n = 1, k = 1, w = 2 (Max score is 2).
dp = [1.0, 0.0]
window_sum = 1.0, result = 0.0

i = 1:
├── dp[1] = 1.0 / 2 = 0.5
├── 1 < 1? False. (i >= k).
├── result += 0.5  -> result = 0.5
├── i - w -> 1 - 2 = -1 < 0. No slide.

Loop ends. Result is 0.5. ✓
Explanation: She starts at 0. Needs to stop at 1. Draws from [1, 2]. 
If she draws 1, score 1 (<= 1) -> Success.
If she draws 2, score 2 (> 1) -> Fail. 
Probability is exactly 50%.

TIME COMPLEXITY: O(N)
The loop strictly runs 'n' times. Inside the loop, we only perform constant time O(1) arithmetic operations 
(addition, subtraction, division).

SPACE COMPLEXITY: O(N)
We allocate a DP array of size 'n + 1' to store the intermediate probabilities.
"""

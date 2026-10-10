# 2162. Minimum Cost to Set Cooking Time
# Difficulty: Medium
# https://leetcode.com/problems/minimum-cost-to-set-cooking-time/

"""
PROBLEM:
A microwave keypad has digits 0 through 9. To enter a cooking time, you press a sequence of digits representing mm:ss.
- The last two digits represent seconds, and any digits before that represent minutes.
- You can omit leading zeros (e.g., 9 minutes and 5 seconds can be entered as "905" instead of "0905").
You are given:
- startAt: The digit where the finger currently rests.
- moveCost: Cost to move the finger from one digit to a different digit.
- pushCost: Cost to push any digit button.
- targetSeconds: The exact cooking time in seconds.
Return the minimum cost to set the cooking time.

EXAMPLES:
Input: startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600 → Output: 6
Explanation:
Target is 600 seconds.
Option 1: 10 mins, 0 secs -> "1000"
Cost: Start at 1. Push 1 (1). Move to 0 (2) + Push (1). Push (1). Push (1) = 6.
Option 2: 9 mins, 60 secs -> "960"
Cost: Start at 1. Move to 9 (2) + Push (1). Move to 6 (2) + Push (1). Move to 0 (2) + Push (1) = 9.
Minimum cost is 6.

Input: startAt = 0, moveCost = 1, pushCost = 2, targetSeconds = 76 → Output: 6
Explanation:
Option 1: 1 min, 16 secs -> "116". Cost = 2 + 1 + 2 + 2 = 7.
Option 2: 0 mins, 76 secs -> "76". Cost = 1 + 2 + 1 + 2 = 6.
Minimum cost is 6.

CONSTRAINTS:
- 0 <= startAt <= 9
- 1 <= moveCost, pushCost <= 10^5
- 1 <= targetSeconds <= 6039

MATH RULES (BOUNDED TIME REPRESENTATIONS & COST SIMULATION):
Because seconds can range from 00 to 99 in a microwave display:
1. Standard decomposition: mins = targetSeconds // 60, secs = targetSeconds % 60.
2. Borrowed decomposition: mins = (targetSeconds // 60) - 1, secs = (targetSeconds % 60) + 60.
No other decompositions exist because borrowing 2 minutes would require secs >= 120 > 99.
Constraints require: 0 <= mins <= 99 and 0 <= secs <= 99.
Since both moveCost and pushCost are >= 1, typing extra leading zeros can never reduce total cost.
We strip all leading zeros from the final formatted 4-digit string ("mm:ss" -> lstrip('0')).
"""

# STEP 1: Define a helper function to calculate the input cost for a given string of digits.
# STEP 2: Generate the two potential (mins, secs) candidates.
# STEP 3: Validate each candidate against the display boundaries (0 <= mins, secs <= 99).
# STEP 4: Convert valid candidates to digit strings, stripping leading zeros.
# STEP 5: Calculate the cost for each valid candidate and return the minimum.

class Solution:
    def minCostSetTime(self, startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> int:
        
        # Helper to calculate the operational cost of entering a specific digit sequence
        def calculate_cost(digits: str) -> int:
            cost = 0
            curr_pos = str(startAt)
            
            for ch in digits:
                if ch != curr_pos:
                    cost += moveCost
                    curr_pos = ch
                cost += pushCost
                
            return cost
            
        candidates = []
        
        # Candidate 1: Standard division
        m1 = targetSeconds // 60
        s1 = targetSeconds % 60
        candidates.append((m1, s1))
        
        # Candidate 2: Borrow 1 minute into seconds (if at least 1 minute exists)
        m2 = m1 - 1
        s2 = s1 + 60
        candidates.append((m2, s2))
        
        min_cost = float('inf')
        
        for mins, secs in candidates:
            # Validate display capacity (both fields must be within 00..99)
            if 0 <= mins <= 99 and 0 <= secs <= 99:
                # Format to a standard 4-character string and strip non-essential leading zeros
                time_str = f"{mins:02d}{secs:02d}".lstrip('0')
                
                # Compute cost and update global minimum
                current_cost = calculate_cost(time_str)
                min_cost = min(min_cost, current_cost)
                
        return min_cost

"""
WHY EACH PART:
- f"{mins:02d}{secs:02d}".lstrip('0'): Guarantees that seconds keep their required padding when minutes > 0 (e.g. 1m 5s -> "0105" -> "105"), while safely trimming useless leading zeros.
- calculate_cost(digits): Simulates the linear physical motion and keypress sequence deterministically.
- candidates.append((m2, s2)): Explores the alternate representation where seconds > 59, which is common in microwaves and frequently cheaper.

KEY TECHNIQUE:
- Search Space Pruning: Reducing a search problem with potential combinatorial branches down to evaluating at most 2 deterministic candidates.
- Simulation: Accurately modeling state transitions (finger movements and presses).

EDGE CASES:
- targetSeconds < 60: m1 = 0, s1 = targetSeconds. Candidate 2 has m2 = -1 (invalid). Evaluates only candidate 1 safely.
- targetSeconds >= 6000: (e.g., 6039): m1 = 100 (> 99, invalid). Only candidate 2 (m2 = 99, s2 = 99) is valid. Handled seamlessly.

TIME COMPLEXITY: O(1) - Only at most two candidate representations are evaluated, and each digit string has length at most 4.
SPACE COMPLEXITY: O(1) - Minimal scalar variables and strings of length <= 4 are created.
"""

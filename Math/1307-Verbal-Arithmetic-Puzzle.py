# 1307. Verbal Arithmetic Puzzle
# Difficulty: Hard
# https://leetcode.com/problems/verbal-arithmetic-puzzle/

"""
PROBLEM:
Given an array of strings `words` and a string `result`.
Return True if there is a valid mapping of characters to digits (0-9) such that:
- Every character maps to exactly one unique digit.
- No word starts with the digit '0' (if its length is > 1).
- The sum of `words` decoded as integers equals `result` decoded as an integer.

EXAMPLES:
Input: words = ["SEND","MORE"], result = "MONEY"
Output: True
(Explanation: The mapping 'S'->9, 'E'->5, 'N'->6, 'D'->7, 'M'->1, 'O'->0, 'R'->8, 'Y'->2 
 turns "SEND" + "MORE" into 9567 + 1085 = 10652 = "MONEY".)

Input: words = ["SIX","SEVEN","SEVEN"], result = "TWENTY"
Output: True
(Explanation: 650 + 68782 + 68782 = 138214)

Input: words = ["LEET","CODE"], result = "POINT"
Output: False

CONSTRAINTS:
- 1 <= words.length <= 5
- 1 <= words[i].length, result.length <= 7
- words[i], result contain only uppercase English letters.
- The number of different characters used is <= 10.

ALGORITHM LOGIC (Backtracking + Column-by-Column Pruning):
1. Trying all 10! permutations of digits is too slow (O(10!) per check).
2. Instead, we mimic manual addition: we add column by column from right to left.
3. If the sum of the digits in the current column (modulo 10) doesn't match the digit assigned 
   to the result string's character in that column, we instantly stop and prune that branch.
4. We track mapped characters (`char_to_digit`), used digits (`used_digits`), and 
   the carry to the next column.
5. Reversing the strings makes index 0 represent the 1s place, index 1 the 10s place, etc.

VISUALIZATION (SEND + MORE = MONEY):
Column 0 (Rightmost):
  D
+ E
---
  Y
We assign a digit to D and E, then check if (D + E) % 10 can be assigned to Y.
If it can, we calculate carry = (D + E) // 10 and move to Column 1 (N + R + carry = E).
If it contradicts previous mappings, we backtrack immediately without assigning S, M, O.
"""

# STEP 1: Fast fail if result is shorter than the longest word (sum cannot be shorter)
# STEP 2: Collect all leading characters to prevent them from being mapped to 0
# STEP 3: Reverse all words and the result to easily iterate from least to most significant digit
# STEP 4: Define the recursive backtrack function (col, row, current_sum)
# STEP 5: Base case: If we finish the current column, check the modulo against the result character
# STEP 6: Recursive step: Traverse rows, assigning unused digits to unmapped characters
# STEP 7: Backtrack (undo assignments) if a path fails

class Solution:
    def isSolvable(self, words: list[str], result: str) -> bool:
        
        max_word_len = max(len(w) for w in words)
        if len(result) < max_word_len:                               # Fast fail: result cannot be shorter than addends
            return False
            
        leading_chars = set()                                        # Track characters that cannot be 0
        for w in words + [result]:
            if len(w) > 1:
                leading_chars.add(w[0])
                
        words = [w[::-1] for w in words]                             # Reverse to process right-to-left
        result = result[::-1]
        
        char_to_digit = {}                                           # Maps character -> digit
        used_digits = set()                                          # Tracks which digits are already assigned
        
        def backtrack(col: int, row: int, current_sum: int) -> bool:
            
            if col == len(result):                                   # Base Case: Processed all columns
                return current_sum == 0                              # Valid if there is no leftover carry
                
            if row == len(words):                                    # Reached the result row for this column
                digit = current_sum % 10                             # Expected digit for the result
                next_carry = current_sum // 10                       # Carry for the next column
                ch = result[col]                                     # Character in the result word
                
                if ch in char_to_digit:                              # If result char is already mapped
                    if char_to_digit[ch] == digit:                   # Matches expected math?
                        return backtrack(col + 1, 0, next_carry)     # Move to next column
                    return False                                     # Contradiction, prune branch
                else:                                                # If result char is not mapped
                    if digit in used_digits:                         # Digit already taken by another letter
                        return False
                    if digit == 0 and ch in leading_chars:           # Cannot assign 0 to a leading character
                        return False
                        
                    char_to_digit[ch] = digit                        # Assign digit
                    used_digits.add(digit)
                    
                    if backtrack(col + 1, 0, next_carry):            # Proceed to next column
                        return True
                        
                    del char_to_digit[ch]                            # BACKTRACK: Undo assignment
                    used_digits.remove(digit)
                    return False
                    
            # Processing standard rows (words)
            if col >= len(words[row]):                               # Current word is shorter than column index
                return backtrack(col, row + 1, current_sum)          # Skip to next word, add 0 to sum
                
            ch = words[row][col]
            
            if ch in char_to_digit:                                  # Character already has a mapped digit
                if char_to_digit[ch] == 0 and ch in leading_chars:
                    return False
                return backtrack(col, row + 1, current_sum + char_to_digit[ch])
                
            else:                                                    # Character needs a digit
                for d in range(10):
                    if d in used_digits:
                        continue
                    if d == 0 and ch in leading_chars:
                        continue
                        
                    char_to_digit[ch] = d                            # Assign digit
                    used_digits.add(d)
                    
                    if backtrack(col, row + 1, current_sum + d):     # Explore path
                        return True
                        
                    del char_to_digit[ch]                            # BACKTRACK: Undo assignment
                    used_digits.remove(d)
                    
                return False                                         # All digits failed, prune branch
                
        return backtrack(0, 0, 0)                                    # Start at column 0, row 0, sum 0

"""
WHY EACH PART:
- [w[::-1] for w in words]: Python indexing makes checking `w[len(w) - 1 - col]` tedious. Reversing strings makes the ones place index 0, tens place index 1, which aligns beautifully with the `col` variable.
- if col == len(result): The algorithm terminates when all columns of the `result` string are processed. If `current_sum` (the final carry) is 0, the math perfectly balances. If it's > 0, the sum exceeded the result's length, which is invalid.
- del char_to_digit[ch] and used_digits.remove(d): This is the essence of backtracking. If a recursive call returns False, we must clean up our temporary assignments so other branches can reuse those digits and characters.

HOW IT WORKS (Column Math Pruning):
Instead of generating all digit permutations and running `sum(words) == result`, we say:
"If D=7 and E=5, then D+E = 12. Therefore, Y MUST be 2. If 2 is already taken by M, stop immediately. Do not bother calculating S, N, O, R."
This pruning reduces the search space from billions of operations to a few thousand.

KEY TECHNIQUE:
- Backtracking / Depth First Search (DFS).
- Constraint Satisfaction Problem (CSP) formulation.
- Math-based Pruning (Right-to-Left evaluation).

EDGE CASES:
- 1-letter words (e.g., "A" + "B" = "C"): Valid, can be mapped to 0 (if valid). Handled by `len(w) > 1` leading character check. ✓
- Result shorter than addend: Immediately returns False via initial length check. ✓
- Words of unequal lengths: Handled gracefully by `col >= len(words[row])`, simply moving to the next word without adding to the sum. ✓

TIME COMPLEXITY: O(10!) - In the absolute worst-case scenario (no pruning possible until the very end), we check 10! mappings. However, due to rigorous column-by-column pruning, the average time complexity is drastically smaller, executing in milliseconds.
SPACE COMPLEXITY: O(C) - Where C is the number of unique characters (max 10). The call stack for recursion will go up to at most `max_word_len * num_words`, which given the constraints is at most 7 * 5 = 35 stack frames. Extremely space efficient.

CONCEPTS USED:
- Backtracking
- Recursion
- Hash Maps and Sets
- Mathematical Modeling (Base-10 column addition)
"""

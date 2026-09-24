# 2001. Number of Pairs of Interchangeable Rectangles
# Difficulty: Medium
# https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/

"""
PROBLEM:
You are given n rectangles represented by a 2D integer array rectangles, where rectangles[i] = [width_i, height_i].
Two rectangles i and j (i < j) are considered interchangeable if they have the same width-to-height ratio. More formally, two rectangles are interchangeable if width_i / height_i == width_j / height_j (using decimal division, not integer division).
Return the number of pairs of interchangeable rectangles in rectangles.

EXAMPLES:
Input: rectangles = [[4,8],[3,6],[10,20],[15,30]] → Output: 6
Explanation: All rectangles have a ratio of 0.5.
The number of pairs is exactly combinations of 4 choose 2: 4 * 3 / 2 = 6.

Input: rectangles = [[4,5],[7,8]] → Output: 0
Explanation: The first rectangle has a ratio of 4/5 = 0.8. The second has a ratio of 7/8 = 0.875. None are interchangeable.

CONSTRAINTS:
- n == rectangles.length
- 1 <= n <= 10^5
- 1 <= width_i, height_i <= 10^5

MATH RULES (HASH MAP COMBINATORICS & FLOAT PRECISION):
An O(N^2) double-loop to compare every pair will cause a Time Limit Exceeded (TLE) error. 
We can reduce this to O(N) by using a Hash Map to store the frequencies of each calculated ratio.
Instead of calculating combinations at the very end using the formula n*(n-1)/2, we can build the total dynamically: 
If we encounter a ratio that has already been seen 'k' times, the current rectangle forms exactly 'k' new pairs. We add 'k' to our total pairs, then increment the frequency of that ratio to 'k+1'.

Note on Float Precision: In statically typed languages, float division can cause precision collision bugs, requiring developers to reduce fractions using the Greatest Common Divisor (GCD). However, Python's 64-bit floats have 53 bits of precision, allowing them to perfectly differentiate all possible fractions up to the 10^5 constraint bound. Standard float division is completely safe and extremely fast here.

VISUALIZATION (rectangles = [[4,8], [3,6], [10,20]]):
Initial: freq_map = {}, pairs = 0

Rectangle 1 [4,8]: ratio = 0.5. Not in map.
- freq_map = {0.5: 1}
- pairs = 0

Rectangle 2 [3,6]: ratio = 0.5. Map has 0.5 with count 1.
- pairs += 1 -> 1
- freq_map = {0.5: 2}

Rectangle 3 [10,20]: ratio = 0.5. Map has 0.5 with count 2.
- pairs += 2 -> 3
- freq_map = {0.5: 3}

Return 3 ✓
"""

from typing import List

# STEP 1: Initialize a dictionary to store the frequency of each width/height ratio.
# STEP 2: Initialize a counter for the total interchangeable pairs.
# STEP 3: Iterate through every rectangle's width and height.
# STEP 4: Calculate the decimal ratio.
# STEP 5: If the ratio exists in the dictionary, add its previous frequency to the pair counter.
# STEP 6: Update the dictionary with the new frequency.

class Solution:
    def interchangeableRectangles(self, rectangles: List[List[int]]) -> int:
        
        freq_map = {}
        interchangeable_pairs = 0
        
        for width, height in rectangles:
            # Calculate the aspect ratio
            ratio = width / height
            
            # If seen before, it forms new pairs with all previous identical ratios
            if ratio in freq_map:
                interchangeable_pairs += freq_map[ratio]
                freq_map[ratio] += 1
            else:
                # First time seeing this ratio
                freq_map[ratio] = 1
                
        return interchangeable_pairs

"""
WHY EACH PART:
- ratio = width / height: Evaluates the geometric property securely using Python's reliable 64-bit float math, bypassing the overhead of math.gcd().
- interchangeable_pairs += freq_map[ratio]: Dynamic pairing logic. Bypasses the need for complex combinatorics formulas by summing the arithmetic progression implicitly.
- freq_map[ratio] = 1: Caches the state for O(1) lookups in future iterations.

KEY TECHNIQUE:
- Hash Map Grouping: Grouping elements by an invariable mathematical property to reduce cross-dependency.
- On-the-fly Combinatorics: Building the summation of combinations during the single traversal.

EDGE CASES:
- No matching rectangles: The dictionary populates, but the 'if' condition is never met. Gracefully returns 0.
- All rectangles match: The arithmetic progression 0 + 1 + 2 + 3... executes smoothly yielding the exact combinations required.

TIME COMPLEXITY: O(N) - We iterate through the array of rectangles exactly once. Hash Map lookups and insertions operate in O(1) average time.
SPACE COMPLEXITY: O(N) - In the worst-case scenario where every rectangle has a unique ratio, the Hash Map will store N key-value pairs.

CONCEPTS USED:
- Hash Maps
- Combinatorics
- Floating Point Math Logic
"""

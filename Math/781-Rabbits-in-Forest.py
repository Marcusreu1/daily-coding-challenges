# 781. Rabbits in Forest
# Difficulty: Medium
# https://leetcode.com/problems/rabbits-in-forest/

"""
PROBLEM:
There is a forest with an unknown number of rabbits. We asked n rabbits "How many rabbits have the same color as you?" 
and collected the answers in an integer array answers where answers[i] is the answer of the ith rabbit.
Given the array answers, return the minimum number of rabbits that could be in the forest.

EXAMPLES:
Input: answers = [1, 1, 2]   → Output: 5
Explanation:
- The two rabbits that answered "1" could both be the same color, say red. So there are 2 red rabbits.
- The rabbit that answered "2" can't be red or the answers would be inconsistent. Say it is blue. 
  There are 3 blue rabbits. 
- Total minimum = 2 (red) + 3 (blue) = 5.

Input: answers = [10, 10, 10] → Output: 11
Explanation:
- All 3 rabbits say "10". They can all belong to the same group of 11 rabbits.
- Total minimum = 11.

CONSTRAINTS:
- 1 <= answers.length <= 10^5
- 0 <= answers[i] <= 1000

LOGIC RULES (GROUPING & CEIL MATH):
1. If a rabbit answers x, the group size for that color is exactly x + 1.
2. If v rabbits all answer x, we can group them together to minimize the total count.
3. However, a single color group can only hold x + 1 rabbits.
4. If v > x + 1, we must create multiple groups of size x + 1.
5. The number of groups needed is math.ceil(v / (x + 1)).
6. Total rabbits contributed by this answer is (number of groups) * (group size).

VISUALIZATION (answers = [1, 1, 1, 1, 1]):
Answer '1' appears 5 times.
- Group size: 1 + 1 = 2 rabbits.
- We have 5 rabbits claiming this size.
- Group 1: [Rabbit A, Rabbit B] (Full)
- Group 2: [Rabbit C, Rabbit D] (Full)
- Group 3: [Rabbit E, Missing Rabbit] (Has space for 1 more, but we must count it!)
- Number of groups = ceil(5 / 2) = 3 groups.
- Total rabbits = 3 groups * 2 size = 6 rabbits. ✓
"""

# STEP 1: Import collections and math modules
# STEP 2: Count the frequencies of each answer using collections.Counter
# STEP 3: Iterate through the dictionary of answers and their counts
# STEP 4: Calculate the required group size (answer + 1)
# STEP 5: Calculate how many groups of this size are needed to fit all the reporting rabbits
# STEP 6: Add the total rabbits for these groups to the grand total

import collections
import math

class Solution:
    def numRabbits(self, answers: list[int]) -> int:
        
        # Count how many rabbits gave the same answer
        count_map = collections.Counter(answers)
        total_rabbits = 0
        
        for answer, rabbits_reporting in count_map.items():
            
            group_size = answer + 1                                     # If rabbit says 'x', group is 'x + 1'
            
            # Find how many distinct color groups of this size we need
            # e.g., if 5 rabbits say 1, we need ceil(5/2) = 3 groups
            num_groups = math.ceil(rabbits_reporting / group_size)
            
            # Add the total capacity of these groups to the final answer
            total_rabbits += num_groups * group_size
            
        return total_rabbits

"""
WHY EACH PART:
- collections.Counter(answers): O(N) way to build a frequency map. Essential for grouping identical answers.
- group_size = answer + 1: A rabbit is counting OTHERS, so the total color population must include the rabbit itself.
- math.ceil(rabbits_reporting / group_size): If 3 rabbits say 1 (group size 2), 3/2 = 1.5. We can't have half a group, 
  so we MUST round up to 2 full groups, bringing the total capacity for that color to 4.

HOW IT WORKS (Example: answers = [1, 0, 1, 0, 0]):

Initial state: count_map = {1: 2, 0: 3}

Iteration 1 (answer = 1, reporting = 2):
├── group_size = 1 + 1 = 2
├── num_groups = ceil(2 / 2) = 1
├── total_rabbits += 1 * 2 = 2
└── total_rabbits is now 2.

Iteration 2 (answer = 0, reporting = 3):
├── group_size = 0 + 1 = 1 (Each is an only child!)
├── num_groups = ceil(3 / 1) = 3
├── total_rabbits += 3 * 1 = 3
└── total_rabbits is now 5.

Returns 5. ✓

EDGE CASES:
- Empty array: Handled perfectly (if constraints allowed it) because the loop wouldn't run -> returns 0. ✓
- answer = 0: Perfectly handled. Size is 1. If 5 rabbits answer 0, it creates 5 distinct groups of 1. ✓
- Very large inputs: Grouping first with Counter reduces a 10^5 array to at most 1000 unique keys, making the loop incredibly fast. ✓

TIME COMPLEXITY: O(N)
Where N is the length of `answers`. Building the Counter takes O(N) time. 
Iterating through the unique answers takes O(U) where U is the number of unique answers (U <= N). 
Overall Time Complexity is O(N).

SPACE COMPLEXITY: O(U)
Where U is the number of unique answers. We store these in the dictionary. 
Since maximum answer is 1000, U <= 1000, making it effectively O(1) in the context of large N.
"""

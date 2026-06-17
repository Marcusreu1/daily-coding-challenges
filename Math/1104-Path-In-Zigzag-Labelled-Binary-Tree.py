# 1104. Path In Zigzag Labelled Binary Tree
# Difficulty: Medium
# https://leetcode.com/problems/path-in-zigzag-labelled-binary-tree/

"""
PROBLEM:
In an infinite binary tree where every node has two children, the nodes are labelled in row order.
In the odd rows (ie., the first, third, fifth,...), the labelling is left to right, 
while in the even rows (second, fourth, sixth,...), the labelling is right to left.
Given the `label` of a node in this tree, return the labels in the path from the root of the tree to the that node.

EXAMPLES:
Input: label = 14
Output: [1, 3, 4, 14]

Input: label = 26
Output: [1, 2, 6, 10, 26]

CONSTRAINTS:
- 1 <= label <= 10^6

MATHEMATICAL INTUITION (THE "TRICK"):
In a STANDARD 1-indexed binary tree:
- The left child of node `x` is `2x`.
- The right child of node `x` is `2x + 1`.
- The parent of node `x` is simply `x // 2`.

However, in a ZIGZAG tree, every alternating row is physically inverted. 
Instead of building the entire tree (which would cause a Memory Limit Exceeded error), 
we can use the properties of the tree levels:
1. A complete binary tree level `d` (where root is level 0) starts at 2^d and ends at 2^(d+1) - 1.
2. Because a row is reversed, the "real" parent of a node is the MIRROR image of its "standard" parent.
3. How do we find the mirror image of a number in a specific row?
   Mirror = (Row Minimum + Row Maximum) - Original Value
4. Therefore, the zigzag parent formula is:
   parent = (min_value_of_parent_row + max_value_of_parent_row) - (label // 2)
"""

# STEP 1: Find the depth (level) of the target label.
# STEP 2: Initialize the result array with the target label.
# STEP 3: Loop upward until we reach the root (label == 1).
# STEP 4: Calculate the standard parent (label // 2).
# STEP 5: Find the boundaries of the parent's level (min and max).
# STEP 6: Apply the mirror formula to find the actual zigzag parent.
# STEP 7: Append the parent to the result, update the label and level.
# STEP 8: Reverse the result array since we built it bottom-up.

from typing import List

class Solution:
    def pathInZigZagTree(self, label: int) -> List[int]:
        
        # Step 1: Find the level of the tree where the label exists (0-indexed)
        # We can find this by seeing how many times we can divide by 2
        level = 0
        temp = label
        while temp > 1:
            temp //= 2
            level += 1
            
        result = [label]
        
        # Step 3: Traverse from bottom to top
        while label > 1:
            
            # Boundaries of the parent's row
            # Min value of row is 2^(level-1)
            parent_min = 2 ** (level - 1)
            # Max value of row is 2^level - 1
            parent_max = (2 ** level) - 1
            
            # Step 4-6: Calculate the inverted parent
            standard_parent = label // 2
            label = (parent_min + parent_max) - standard_parent
            
            # Step 7: Store and move up
            result.append(label)
            level -= 1
            
        # Step 8: Reverse to get root-to-node path
        return result[::-1]

"""
WHY EACH PART:
- temp //= 2: A fast mathematical way to find the depth of a node in a binary tree (equivalent to log2).
- parent_min = 2 ** (level - 1): Uses binary tree properties to find the start of the previous row.
- parent_max = (2 ** level) - 1: Uses binary tree properties to find the end of the previous row.
- (parent_min + parent_max) - standard_parent: The core symmetry formula. It flips the standard parent horizontally across the tree.

HOW IT WORKS (Example: label = 14):
Initial: label = 14
Level Calculation: 14 -> 7 -> 3 -> 1. Level = 3.
result = [14]

Iteration 1 (Current Label: 14, Level: 3):
├── We need the parent at Level 2.
├── parent_min = 2^2 = 4
├── parent_max = 2^3 - 1 = 7
├── standard_parent = 14 // 2 = 7
├── new_label = (4 + 7) - 7 = 4
├── result = [14, 4]
└── level = 2

Iteration 2 (Current Label: 4, Level: 2):
├── We need the parent at Level 1.
├── parent_min = 2^1 = 2
├── parent_max = 2^2 - 1 = 3
├── standard_parent = 4 // 2 = 2
├── new_label = (2 + 3) - 2 = 3
├── result = [14, 4, 3]
└── level = 1

Iteration 3 (Current Label: 3, Level: 1):
├── We need the parent at Level 0.
├── parent_min = 2^0 = 1
├── parent_max = 2^1 - 1 = 1
├── standard_parent = 3 // 2 = 1
├── new_label = (1 + 1) - 1 = 1
├── result = [14, 4, 3, 1]
└── level = 0

Exit Loop. 
result[::-1] = [1, 3, 4, 14] ✓

TIME COMPLEXITY: O(log N) - We only traverse the height of the tree, which is log2(label). Very efficient.
SPACE COMPLEXITY: O(log N) - The result array stores exactly the height of the tree number of elements.

CONCEPTS USED:
- Binary Tree Math
- Symmetrical Inversion / Mirroring
- Bottom-Up Traversal
"""

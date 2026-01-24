# 96. Unique Binary Search Trees
# Difficulty: Medium
# https://leetcode.com/problems/unique-binary-search-trees/

"""
PROBLEM:
Given an integer n, return the number of structurally unique BSTs
(Binary Search Trees) which have exactly n nodes with unique values from 1 to n.

EXAMPLES:
Input: n = 3  → Output: 5
Input: n = 1  → Output: 1

CONSTRAINTS:
- 1 <= n <= 19

WHAT IS A BST?
A Binary Search Tree where for each node:
- All values in left subtree are SMALLER
- All values in right subtree are LARGER

VISUALIZATION FOR n = 3 (5 unique BSTs):

    1         1          2          3        3
     \         \        / \        /        /
      2         3      1   3      1        2
       \       /                   \      /
        3     2                     2    1

KEY INSIGHT:
For n nodes, if we choose node i as root:
- Left subtree has (i-1) nodes (values 1 to i-1)
- Right subtree has (n-i) nodes (values i+1 to n)

Number of BSTs with root i = G(i-1) × G(n-i)

Total: G(n) = Σ G(i-1) × G(n-i) for i = 1 to n

This is the CATALAN NUMBER sequence!
G(0)=1, G(1)=1, G(2)=2, G(3)=5, G(4)=14, G(5)=42, ...
"""

# STEP 1: Create DP array where dp[i] = number of unique BSTs with i nodes
# STEP 2: Base cases: dp[0] = dp[1] = 1
# STEP 3: For each number of nodes, sum all possible root choices
# STEP 4: Return dp[n]

class Solution:
    def numTrees(self, n: int) -> int:
        
        dp = [0] * (n + 1)                                                       # dp[i] = unique BSTs with i nodes
        
        dp[0] = 1                                                                # Empty tree = 1 way
        dp[1] = 1                                                                # Single node = 1 way
        
        for nodos in range(2, n + 1):                                            # For each tree size
            for raiz in range(1, nodos + 1):                                     # Try each node as root
                izquierda = raiz - 1                                             # Nodes in left subtree
                derecha = nodos - raiz                                           # Nodes in right subtree
                dp[nodos] += dp[izquierda] * dp[derecha]                         # Multiply possibilities
        
        return dp[n]                                                             # Return answer for n nodes

"""
WHY EACH PART:
- dp[0] = 1: Empty subtree counts as 1 way (needed for multiplication)
- dp[1] = 1: Single node = 1 unique BST
- for nodos: Build solution for 2, 3, ..., n nodes
- for raiz: Try each value 1 to nodos as root
- izquierda = raiz - 1: Values 1 to raiz-1 go left
- derecha = nodos - raiz: Values raiz+1 to nodos go right
- dp[izq] * dp[der]: Each left tree combines with each right tree

HOW IT WORKS (Example: n = 4):

Base: dp = [1, 1, 0, 0, 0]

nodos = 2:
├── raiz=1: dp[0]×dp[1] = 1×1 = 1
├── raiz=2: dp[1]×dp[0] = 1×1 = 1
└── dp[2] = 2

dp = [1, 1, 2, 0, 0]

nodos = 3:
├── raiz=1: dp[0]×dp[2] = 1×2 = 2
├── raiz=2: dp[1]×dp[1] = 1×1 = 1
├── raiz=3: dp[2]×dp[0] = 2×1 = 2
└── dp[3] = 5

dp = [1, 1, 2, 5, 0]

nodos = 4:
├── raiz=1: dp[0]×dp[3] = 1×5 = 5
├── raiz=2: dp[1]×dp[2] = 1×2 = 2
├── raiz=3: dp[2]×dp[1] = 2×1 = 2
├── raiz=4: dp[3]×dp[0] = 5×1 = 5
└── dp[4] = 14

Return: 14 ✓

KEY TECHNIQUE:
- Dynamic Programming: Build from smaller subproblems
- Catalan numbers: Classic combinatorial sequence
- Product principle: Left choices × Right choices

EDGE CASES:
- n = 1: Returns 1 (just the root) ✓
- n = 2: Returns 2 (left child or right child) ✓
- n = 19: Returns 1767263190 (within int range) ✓

TIME COMPLEXITY: O(n²) - Nested loops
SPACE COMPLEXITY: O(n) - DP array

CONCEPTS USED:
- Dynamic Programming
- Catalan numbers
- Binary Search Tree properties
- Combinatorics (product principle)
- Recursion to iteration conversion
"""

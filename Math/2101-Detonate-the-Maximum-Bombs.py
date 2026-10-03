# 2101. Detonate the Maximum Bombs
# Difficulty: Medium
# https://leetcode.com/problems/detonate-the-maximum-bombs/

"""
PROBLEM:
You are given a list of bombs. The range of a bomb is defined as the area where its effect can be felt. This area is in the shape of a circle with the center as the location of the bomb.
The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri]. xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas ri denotes the radius of its range.
You may choose to detonate a single bomb. When a bomb is detonated, it will detonate all bombs that lie in its range. These bombs will further detonate the bombs that lie in their ranges.
Given the list of bombs, return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb.

EXAMPLES:
Input: bombs = [[2,1,3],[6,1,4]] → Output: 2
Explanation:
The upper bomb is at (2,1) with radius 3. The lower is at (6,1) with radius 4.
- If we detonate the left bomb, its radius (3) does not reach the right bomb. (Only 1 detonated).
- If we detonate the right bomb, its radius (4) reaches the left bomb. (2 detonated).
Maximum is 2.

Input: bombs = [[1,1,5],[10,10,5]] → Output: 1
Explanation: They are too far apart to reach each other.

Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]] → Output: 5

CONSTRAINTS:
- 1 <= bombs.length <= 100
- bombs[i].length == 3
- 1 <= xi, yi, ri <= 10^5

MATH RULES (DIRECTED GRAPHS & SQUARED DISTANCES):
Because radii differ, connection is NOT reciprocal. A large bomb might reach a small bomb, but not vice versa. This necessitates modeling the problem as a Directed Graph.
To determine if Bomb 'i' reaches Bomb 'j', we check if the Euclidean distance between their centers is less than or equal to the radius of Bomb 'i'.
Formula: sqrt((x1 - x2)^2 + (y1 - y2)^2) <= R1
To avoid precision loss and slow computation from floating-point square roots, we square both sides entirely:
(x1 - x2)^2 + (y1 - y2)^2 <= R1^2

VISUALIZATION (DFS Chain Reaction):
Graph logic maps out:
0 -> [1, 2]
1 -> [3]
2 -> []
3 -> [0] (Cycle!)

DFS starting at 0:
- Visit 0 (Set: {0})
- Explore 1 (Set: {0, 1})
- Explore 3 (Set: {0, 1, 3})
- Explore 0 (Already visited, ignore to prevent infinite loop)
- Explore 2 (Set: {0, 1, 3, 2})
Total count: 4. ✓
"""

import collections
from typing import List

# STEP 1: Initialize an adjacency list to represent the directed graph of bomb blasts.
# STEP 2: Use nested loops to evaluate the squared distance between all pairs of bombs.
# STEP 3: If bomb 'i' can reach bomb 'j', append 'j' to 'i's list of directed edges.
# STEP 4: Define a DFS helper function that traverses the graph, adding nodes to a 'visited' set to track detonations and prevent cycles.
# STEP 5: Iterate through every bomb, running DFS to simulate starting the chain reaction from that bomb, and keep track of the maximum detonated count.

class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        n = len(bombs)
        
        # Build the directed graph
        graph = collections.defaultdict(list)
        
        for i in range(n):
            x1, y1, r1 = bombs[i]
            # Precalculate squared radius to avoid recalculating it inside the inner loop
            r1_squared = r1 ** 2 
            
            for j in range(n):
                if i == j:
                    continue
                    
                x2, y2, _ = bombs[j]
                
                # Check if bomb 'j' is within the blast radius of bomb 'i'
                if (x1 - x2)**2 + (y1 - y2)**2 <= r1_squared:
                    graph[i].append(j)
                    
        # Depth First Search to simulate the chain reaction
        def dfs(node: int, visited: set) -> int:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, visited)
            return len(visited)
            
        max_detonated = 0
        
        # Test the chain reaction starting from every individual bomb
        for i in range(n):
            visited = set()
            detonated_count = dfs(i, visited)
            
            if detonated_count > max_detonated:
                max_detonated = detonated_count
                
            # Early break optimization: Cannot possibly detonate more bombs than exist
            if max_detonated == n:
                break
                
        return max_detonated

"""
WHY EACH PART:
- graph = collections.defaultdict(list): Automatically handles missing keys securely, simplifying the graph generation.
- (x1 - x2)**2 + (y1 - y2)**2 <= r1_squared: The absolute fastest and safest way to calculate distance-radius overlap in competitive programming.
- if neighbor not in visited: The core safety mechanism of graph traversal. It instantly halts infinite loops caused by symmetrically placed bombs.
- if max_detonated == n: break: If starting at bomb 2 detonates all 100 bombs, there is no mathematical need to test starting at bombs 3 through 100.

KEY TECHNIQUE:
- Directed Graph Modeling: Translating a continuous physical geometry constraint into discrete nodes and directed edges.
- Depth-First Search (DFS): Algorithmically traversing the nested chain reactions.

EDGE CASES:
- Only 1 bomb provided: Nested loop bypasses (i == j). DFS runs once, visits node 0. Returns 1. Correct.
- Multiple separated clusters: DFS naturally halts at the boundaries of the cluster it started in. The loop over all `n` bombs ensures the largest cluster is eventually found.

TIME COMPLEXITY: O(N^3) - Building the graph requires comparing every bomb to every other bomb: O(N^2). The DFS traversal, in the worst case (a fully connected graph), takes O(V + E) which translates to O(N + N^2). We run this DFS for every bomb N, resulting in O(N^3). Since N <= 100, N^3 is only 1,000,000 operations, which runs instantaneously in Python.
SPACE COMPLEXITY: O(N^2) - To store the adjacency list for the directed graph (which could have up to N^2 edges). The DFS call stack and 'visited' set take O(N).
"""

# 973. K Closest Points to Origin
# Difficulty: Medium
# https://leetcode.com/problems/k-closest-points-to-origin/

"""
PROBLEM:
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., sqrt((x1 - x2)^2 + (y1 - y2)^2)).
You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

EXAMPLES:
Input: points = [[1,3],[-2,2]], k = 1 → Output: [[-2,2]]
Explanation: 
The squared distance between (1, 3) and the origin is 1^2 + 3^2 = 10.
The squared distance between (-2, 2) and the origin is (-2)^2 + 2^2 = 8.
8 < 10, therefore (-2, 2) is closer to the origin. We only want the closest k = 1 points, so we return [[-2,2]].

Input: points = [[3,3],[5,-1],[-2,4]], k = 2 → Output: [[3,3],[-2,4]]
Explanation: The squared distances are 18, 26, and 20 respectively. The two smallest are 18 and 20.

CONSTRAINTS:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

MATH RULES (BOUNDED MAX-HEAP & EUCLIDEAN OPTIMIZATION):
1. Euclidean Optimization: Calculating square roots is computationally expensive. Since we only need to compare relative distances, we can strictly compare the sum of squares: x^2 + y^2.
2. The "Top K" Pattern: Sorting the entire array of N points takes O(N log N) time, which is inefficient if N is massive and K is tiny. 
   Instead, we maintain a Bounded Max-Heap of size K. We iterate through the points and push them into the heap. Whenever the heap size exceeds K, we pop the root (which represents the maximum distance in the heap).
   By continuously destroying the furthest points, the heap will naturally retain only the K closest points.
   Since Python's `heapq` is natively a Min-Heap, we simulate a Max-Heap by pushing the distances as negative values (e.g., a distance of 10 becomes -10, which evaluates as mathematically smaller than -5, placing it at the top of the Min-Heap to be popped).
"""

import heapq
from typing import List

# STEP 1: Initialize an empty list to act as our Priority Queue (Heap).
# STEP 2: Iterate through every point in the array.
# STEP 3: Calculate the squared distance from the origin.
# STEP 4: Push the point into the heap using negative distance to simulate a Max-Heap.
# STEP 5: If the heap exceeds size 'k', pop the root (discarding the furthest point).
# STEP 6: Extract and return only the [x, y] coordinates from the surviving tuples in the heap.

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        
        heap = []
        
        # O(N log K) iteration through the points
        for x, y in points:
            # Calculate squared distance to avoid floating-point math overhead
            squared_distance = x**2 + y**2
            
            # Push tuple: (-distance, x, y). 
            # Negative distance forces the largest actual distance to the top of the Min-Heap.
            heapq.heappush(heap, (-squared_distance, x, y))
            
            # Maintain a strict bounded size of K elements
            if len(heap) > k:
                heapq.heappop(heap)
                
        # Extract the coordinates from the heap tuples
        # Tuple structure is (neg_dist, x, y). We only need x and y.
        return [[x, y] for _, x, y in heap]

"""
WHY EACH PART:
- squared_distance = x**2 + y**2: Replaces the O(1) math.sqrt() calculation with an even faster O(1) integer arithmetic operation, removing precision drift.
- heapq.heappush / heapq.heappop: Pushing and popping from a heap takes strictly O(log K) time. 
- len(heap) > k: The safety valve. It guarantees the heap never stores more than K+1 elements in memory, dropping space complexity drastically compared to sorting.

KEY TECHNIQUE:
- Priority Queue (Bounded Max-Heap): The ultimate architectural pattern for any "Top K" problem in computer science.
- Negative Inversion: A Python-specific trick to reverse the sorting behavior of standard libraries without creating custom comparator classes.

EDGE CASES:
- k equals points.length: The heap will ingest all elements and never pop. Returning the entire array successfully.
- Duplicate distances (e.g., [1,0] and [0,1]): Both will be pushed. The heap will use the 'x' and 'y' values as tie-breakers for sorting internally, preventing crash bugs, and keeping both safely.

TIME COMPLEXITY: O(N log K) - We process all N points. For each point, pushing and potentially popping from a heap of size K takes O(log K) time. Much faster than O(N log N) sorting when K is small.
SPACE COMPLEXITY: O(K) - The heap strictly bounds its memory footprint to K elements, regardless of how massive N is.
"""

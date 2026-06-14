# 1093. Statistics from a Large Sample
# Difficulty: Medium
# https://leetcode.com/problems/statistics-from-a-large-sample/

"""
PROBLEM:
You are given a large sample of integers in the range [0, 255]. Since the sample is so large, 
it is given as an array `count` where `count[k]` is the number of times that integer `k` appears in the sample.
Return the statistics of the sample as an array of floating-point numbers:
[minimum, maximum, mean, median, mode].

EXAMPLES:
Input: count = [0,1,3,4,0,0,0,0... (256 elements)]
Output: [1.00000, 3.00000, 2.37500, 2.50000, 3.00000]
Explanation: 
The sample is [1, 2, 2, 2, 3, 3, 3, 3].
- Min: 1.0
- Max: 3.0
- Mean: (1 + 6 + 12) / 8 = 2.375
- Median: The 4th and 5th elements are 2 and 3. Average is 2.5
- Mode: 3 appears most frequently (4 times).

CONSTRAINTS:
- count.length == 256
- 1 <= sum(count) <= 10^9
- count[i] fits in a 32-bit integer

MATHEMATICAL INTUITION (THE "TRICK"):
The naive approach is to reconstruct the original array. However, sum(count) can be 10^9. 
Creating an array of 1 billion elements will cause a Memory Limit Exceeded (MLE) error.
Instead, we must calculate everything directly from the frequency map:
1. Minimum: The first index `i` from the left where count[i] > 0.
2. Maximum: The first index `i` from the right where count[i] > 0.
3. Mode: The index `i` with the largest count[i].
4. Mean: The sum of (i * count[i]) divided by the total number of elements.
5. Median: The hardest part. We need the middle element(s). By keeping a running total 
   (prefix sum) of the elements seen so far, we can find the exact values at the middle indices 
   without expanding the array.
"""

from typing import List

class Solution:
    def sampleStats(self, count: List[int]) -> List[float]:
        
        total_elements = sum(count)
        
        minimum = -1.0
        maximum = -1.0
        mode = -1.0
        max_count = 0
        total_sum = 0
        
        # Step 1: Calculate Min, Max, Mode, and Mean
        for i in range(256):
            if count[i] > 0:
                # First non-zero count from left is the minimum
                if minimum == -1.0:
                    minimum = float(i)
                
                # Continuously update maximum, the last one seen will be the max
                maximum = float(i)
                
                # Accumulate sum for the mean
                total_sum += i * count[i]
                
                # Update mode if current count is the highest seen
                if count[i] > max_count:
                    max_count = count[i]
                    mode = float(i)
                    
        mean = total_sum / total_elements
        
        # Step 2: Calculate the Median
        # 0-indexed positions for the median
        # If total_elements is 5: m1_pos = 2, m2_pos = 2 (We just need the 3rd element)
        # If total_elements is 4: m1_pos = 1, m2_pos = 2 (We need 2nd and 3rd elements)
        median1_pos = (total_elements - 1) // 2
        median2_pos = total_elements // 2
        
        median1_val = -1
        median2_val = -1
        current_count = 0
        
        for i in range(256):
            if count[i] > 0:
                current_count += count[i]
                
                # If we just passed the first median position
                if median1_val == -1 and current_count > median1_pos:
                    median1_val = i
                    
                # If we just passed the second median position
                if median2_val == -1 and current_count > median2_pos:
                    median2_val = i
                    break # We found both, stop searching
                    
        median = (median1_val + median2_val) / 2.0
        
        return [minimum, maximum, mean, median, mode]

"""
WHY EACH PART:
- sum(count): Gets the total `N` in O(1) time complexity conceptually, as array length is fixed at 256.
- maximum updating continually: Avoids a separate backwards loop. The last `i` processed will naturally be the max.
- current_count > median_pos: Instead of expanding `[2, 2, 2]`, we know that if we needed the 2nd element, and `current_count` jumped from 0 to 3 at index `2`, our median is `2`.

HOW THE MEDIAN LOGIC WORKS (Example: count total = 4):
m1_pos = (4-1)//2 = 1 (Target: 2nd element)
m2_pos = 4//2 = 2     (Target: 3rd element)

Suppose count is: 
Index 1: count 1
Index 3: count 2
Index 4: count 1

Iteration i=1:
├── current_count = 1
├── > m1_pos (1 > 1)? False
└── > m2_pos (1 > 2)? False

Iteration i=3:
├── current_count = 1 + 2 = 3
├── > m1_pos (3 > 1)? True! -> median1_val = 3
└── > m2_pos (3 > 2)? True! -> median2_val = 3 (Break loop)

median = (3 + 3) / 2 = 3.0 ✓

KEY TECHNIQUE:
- Frequency Map Iteration: Never unpack a frequency map if you just need statistics.
- Prefix Sum (Running Total): Used to locate specific percentiles/medians in a compressed dataset.

TIME COMPLEXITY: O(1) - The array size is strictly fixed at 256. We do a couple of passes of 256 elements. Constant time!
SPACE COMPLEXITY: O(1) - No extra scaling arrays are created, only a few variables.
"""

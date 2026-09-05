# 1860. Incremental Memory Leak
# Difficulty: Medium
# https://leetcode.com/problems/incremental-memory-leak/

"""
PROBLEM:
You are given two integers memory1 and memory2 representing the available memory in bits on two memory sticks. There is an infinite loop where memory is allocated sequentially.
On the ith second (starting from 1), i bits of memory are allocated to the stick with more available memory.
If both sticks have the same available memory, the bits are allocated to the first stick (memory1).
If neither stick has at least i bits of available memory, the program crashes.
Return an array containing [crashTime, memory1, memory2], where crashTime is the time (in seconds) when the program crashed and memory1 and memory2 are the available bits in the first and second sticks respectively.

EXAMPLES:
Input: memory1 = 2, memory2 = 2 → Output: [3, 1, 0]
Explanation: 
- 1st second: memory1 has the same as memory2. memory1 gets 1 bit allocated. State: (1, 2)
- 2nd second: memory2 has more memory. memory2 gets 2 bits allocated. State: (1, 0)
- 3rd second: memory1 has 1 bit, memory2 has 0 bits. Neither has 3 bits. Crash.
Result: [3, 1, 0].

Input: memory1 = 8, memory2 = 11 → Output: [6, 0, 4]
Explanation: 
- 1st second: memory2 gets 1 bit. (8, 10)
- 2nd second: memory2 gets 2 bits. (8, 8)
- 3rd second: memory1 gets 3 bits. (5, 8)
- 4th second: memory2 gets 4 bits. (5, 4)
- 5th second: memory1 gets 5 bits. (0, 4)
- 6th second: Neither has 6 bits. Crash.
Result: [6, 0, 4].

CONSTRAINTS:
- 0 <= memory1, memory2 <= 2^31 - 1

MATH RULES (SUBLINEAR COMPLEXITY & GAUSS SUMMATION):
At first glance, limits of 2^31 suggest an O(1) mathematical approach is mandatory to prevent Time Limit Exceeded (TLE). 
However, the amount of memory consumed grows arithmetically (1 + 2 + 3 + ... + i). The total memory consumed after 'i' seconds is given by the Gauss formula: i * (i + 1) / 2.
Setting i * (i + 1) / 2 = 2 * 10^9 reveals that the maximum possible number of seconds before a crash is roughly 63,245.
A while loop running 65,000 times executes in under 1 millisecond. Therefore, direct simulation is highly optimal and mathematically sound.

VISUALIZATION (memory1 = 2, memory2 = 2):
time_sec = 1: memory1 (2) >= memory2 (2). 2 >= 1. memory1 = 2 - 1 = 1.
time_sec = 2: memory1 (1) < memory2 (2). 2 >= 2. memory2 = 2 - 2 = 0.
time_sec = 3: memory1 (1) >= memory2 (0). memory1 < 3 -> Break!
Return [3, 1, 0] ✓
"""

from typing import List

# STEP 1: Initialize a counter for the seconds starting at 1.
# STEP 2: Open an infinite loop to simulate the memory allocation process.
# STEP 3: Check which memory stick has more space (or if they are equal, prioritize memory1).
# STEP 4: If the chosen memory stick has less space than the current second, break the loop (crash).
# STEP 5: Otherwise, deduct the current second's bits from the chosen stick and increment the time.
# STEP 6: Return the crash time and the remaining memory on both sticks.

class Solution:
    def memLeak(self, memory1: int, memory2: int) -> List[int]:
        
        time_sec = 1
        
        while True:
            # Tie-breaker prioritizes memory1, so we use >=
            if memory1 >= memory2:
                # Check if it lacks capacity for the current second allocation
                if memory1 < time_sec:
                    break
                memory1 -= time_sec
                
            else:
                # memory2 is strictly greater
                if memory2 < time_sec:
                    break
                memory2 -= time_sec
                
            # Move to the next second
            time_sec += 1
            
        return [time_sec, memory1, memory2]

"""
WHY EACH PART:
- time_sec = 1: The problem explicitly states that allocation starts on the 1st second, not the 0th.
- if memory1 >= memory2: Naturally handles both the "memory1 has more" case and the "both are equal, give it to memory1" tie-breaker rule simultaneously.
- if memory < time_sec: break: Triggers the simulated crash the exact moment constraints fail, keeping time_sec perfectly aligned with the crash time required for the output.

KEY TECHNIQUE:
- Pure Simulation: Leveraging the arithmetic progression math bound to safely iterate without needing complex O(1) binary search roots or quadratic equations.

EDGE CASES:
- memory1 = 0, memory2 = 0: time_sec is 1. memory1 >= memory2. memory1 (0) < time_sec (1). Breaks immediately. Returns [1, 0, 0]. Works flawlessly.

TIME COMPLEXITY: O(sqrt(memory1 + memory2)) - The loop runs exactly as many times as the triangular number progression allows, strictly bounded by the square root of the total memory.
SPACE COMPLEXITY: O(1) - Only a single integer (time_sec) is allocated in memory.

CONCEPTS USED:
- System Simulation
- Arithmetic Progressions
- Condition Branching
"""

# 1304. Find N Unique Integers Sum up to Zero
# Difficulty: Easy
# https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero/

"""
PROBLEM:
Given an integer n, generate and return an array containing exactly n unique integers 
such that their total sum is exactly 0. Any valid array that satisfies this condition is acceptable.

EXAMPLES:
Input: n = 5
Output: [-2, -1, 1, 2, 0]
(Explanation: The sum of these 5 unique integers is (-2) + (-1) + 1 + 2 + 0 = 0. 
Other valid arrays could be [-7, -1, 1, 3, 4] etc., but generating symmetric pairs is the easiest.)

Input: n = 3
Output: [-1, 1, 0]

Input: n = 1
Output: [0]

CONSTRAINTS:
- 1 <= n <= 1000

ALGORITHM LOGIC (Symmetric Pairs):
1. The most efficient way to ensure a sum of 0 is to use additive inverses (x and -x).
2. We can generate pairs of numbers (1 and -1, 2 and -2, etc.) up to n // 2.
3. If n is an even number, these pairs will exactly fill the array, and their sum will be 0.
4. If n is an odd number, we will have one empty slot left after generating the pairs. 
   We can simply append a 0 to fill the array without changing the total sum.

VISUALIZATION (n = 5):
Pairs to generate = 5 // 2 = 2 pairs.

Iteration 1 (i = 1):
Append 1 and -1
Array: [1, -1]

Iteration 2 (i = 2):
Append 2 and -2
Array: [1, -1, 2, -2]

Is n (5) odd? Yes (5 % 2 != 0).
Append 0.
Final Array: [1, -1, 2, -2, 0] ✓
Sum: 0
Unique Elements: 5
"""

# STEP 1: Initialize an empty list to store the result
# STEP 2: Loop from 1 up to n // 2 (inclusive)
# STEP 3: In each iteration, append the positive number 'i' and its negative counterpart '-i'
# STEP 4: After the loop, check if n is odd (n % 2 != 0)
# STEP 5: If it is odd, append 0 to balance the array length without affecting the sum
# STEP 6: Return the constructed array

class Solution:
    def sumZero(self, n: int) -> list[int]:
        
        result = []                                                  # Array to store our unique integers
        
        for i in range(1, (n // 2) + 1):                             # Generate symmetric pairs up to half of n
            result.append(i)                                         # Add positive inverse
            result.append(-i)                                        # Add negative inverse
            
        if n % 2 != 0:                                               # Check if n is odd
            result.append(0)                                         # Add the neutral pivot
            
        return result                                                # Return the final balanced array

"""
WHY EACH PART:
- range(1, (n // 2) + 1): We need to generate exactly half of the array's length in pairs. The +1 ensures the range includes the actual halfway point, as Python's range stop parameter is exclusive.
- result.append(i) and append(-i): Guarantees that the running sum of the array is permanently locked at 0.
- if n % 2 != 0: Handling the parity constraint. Even lengths are perfectly satisfied by pairs. Odd lengths require exactly one more element, and 0 is the only element that doesn't ruin the sum constraint.

HOW IT WORKS (Example: n = 2):
Pairs to generate = 2 // 2 = 1.
Loop i = 1: append 1, append -1. Array = [1, -1].
Is 2 odd? No.
Returns [1, -1]. Sum is 0. ✓

KEY TECHNIQUE:
- Constructive Algorithms: Building a valid output step-by-step using a known mathematical property (additive inverses) instead of searching for a valid combination randomly.

EDGE CASES:
- n = 1: The loop range is (1, 0), so it doesn't execute. It goes straight to the odd check, appends 0, and returns [0]. Perfect. ✓
- Large n (e.g., n = 1000): The loop easily generates 500 pairs in fractions of a millisecond without deep memory overhead. ✓

TIME COMPLEXITY: O(N) - We iterate roughly N / 2 times, performing O(1) append operations. This scales linearly with the size of N.
SPACE COMPLEXITY: O(N) - The output array requires O(N) space to store the generated integers. No extra auxiliary scaling space is used.

CONCEPTS USED:
- Additive Inverses
- Modulo Arithmetic (Parity checking)
- Array manipulation
"""

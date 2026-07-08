# 1281. Subtract the Product and Sum of Digits of an Integer
# Difficulty: Easy
# https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/

"""
PROBLEM:
Given an integer number n, return the difference between the product of its digits and the sum of its digits.

EXAMPLES:
Input: n = 234
Output: 15 
(Explanation: 
Product of digits = 2 * 3 * 4 = 24 
Sum of digits = 2 + 3 + 4 = 9 
Result = 24 - 9 = 15)

Input: n = 4421
Output: 21
(Explanation: 
Product of digits = 4 * 4 * 2 * 1 = 32 
Sum of digits = 4 + 4 + 2 + 1 = 11 
Result = 32 - 11 = 21)

CONSTRAINTS:
- 1 <= n <= 10^5

ALGORITHM LOGIC (Digit Extraction via Modulo):
1. To process a number digit by digit mathematically, we use base-10 arithmetic.
2. Modulo 10 (% 10) extracts the rightmost digit of a number.
3. Integer division by 10 (// 10) removes the rightmost digit from a number.
4. We can use a while loop to repeatedly extract and remove digits until the number becomes 0.
5. We maintain two rolling accumulators: one for the product (initialized to 1) and one for the sum (initialized to 0).
6. Return the difference once the loop concludes.

VISUALIZATION (n = 234):
Initial State: 
product = 1, sum = 0, n = 234

Iteration 1:
digit = 234 % 10 = 4
product = 1 * 4 = 4
sum = 0 + 4 = 4
n = 234 // 10 = 23

Iteration 2:
digit = 23 % 10 = 3
product = 4 * 3 = 12
sum = 4 + 3 = 7
n = 23 // 10 = 2

Iteration 3:
digit = 2 % 10 = 2
product = 12 * 2 = 24
sum = 7 + 2 = 9
n = 2 // 10 = 0

Loop Ends (n is 0).
Result = 24 - 9 = 15 ✓
"""

# STEP 1: Initialize accumulators (product to 1, sum to 0)
# STEP 2: Loop while n is greater than 0
# STEP 3: Extract the rightmost digit using n % 10
# STEP 4: Update both the product and the sum with the extracted digit
# STEP 5: Remove the rightmost digit from n using n // 10
# STEP 6: Return the product minus the sum

class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        
        producto = 1                                                 # Multiplicative identity
        suma = 0                                                     # Additive identity
        
        while n > 0:                                                 # Process until no digits remain
            
            digito = n % 10                                          # Extract the last digit
            
            producto *= digito                                       # Multiply into running product
            suma += digito                                           # Add into running sum
            
            n //= 10                                                 # Chop off the last digit
            
        return producto - suma                                       # Return the final difference

"""
WHY EACH PART:
- producto = 1: If we initialize a multiplicative accumulator to 0, anything multiplied by it will remain 0. It must be 1.
- while n > 0: Ensures we process every digit. When integer division finally divides a single digit (like 2 // 10), it results in 0, breaking the loop safely.
- n % 10: The mathematical standard for pulling the least significant digit in base-10.
- n //= 10: The mathematical standard for shifting a base-10 number one position to the right, discarding the decimal.

HOW IT WORKS (Example: n = 7):
digit = 7 % 10 = 7
producto = 1 * 7 = 7
suma = 0 + 7 = 7
n = 7 // 10 = 0
Returns: 7 - 7 = 0. ✓

KEY TECHNIQUE:
- Modulo Arithmetic: Extracting digits mathematically is generally faster and uses less memory than converting the integer to a String and iterating through characters.

EDGE CASES:
- Single digit numbers (e.g., n = 5): Product is 5, sum is 5, result is 0. Works perfectly. ✓
- Numbers containing zero (e.g., n = 102): Product will instantly become 0 and remain 0. Sum continues normally. Works perfectly. ✓

TIME COMPLEXITY: O(log10(N)) - The loop runs once for each digit in the number. The number of digits in N is proportional to the base-10 logarithm of N. For our constraint (10^5), this loop runs at most 6 times. Extremely fast.
SPACE COMPLEXITY: O(1) - We only store three integer variables (`producto`, `suma`, `digito`) regardless of the size of `n`.

CONCEPTS USED:
- Number Theory / Base-10 Arithmetic
- While Loops
- Rolling Accumulators
"""

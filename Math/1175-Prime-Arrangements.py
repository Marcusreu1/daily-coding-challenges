# 1175. Prime Arrangements
# Difficulty: Easy
# https://leetcode.com/problems/prime-arrangements/

"""
PROBLEM:
Return the number of permutations of 1 to n so that prime numbers are at prime indices (1-indexed).
(Recall that an integer is prime if and only if it is greater than 1, and cannot be written as a product of two positive integers both smaller than it.)
Since the answer may be large, return the answer modulo 10^9 + 7.

EXAMPLES:
Input: n = 5
Output: 12
Explanation: For example [1,2,5,4,3] is a valid permutation, but [5,2,3,4,1] is not because the prime number 5 is at index 1.
Primes up to 5: [2, 3, 5] (3 primes). Composites: [1, 4] (2 composites).
Arrangements = 3! * 2! = 6 * 2 = 12.

Input: n = 100
Output: 682289015

CONSTRAINTS:
- 1 <= n <= 100

ALGORITHMIC INTUITION (THE "TRICK"):
This problem sounds like complex backtracking/permutations, but it's purely a Combinatorics math problem.
The problem forces a strict separation:
- All prime numbers MUST go to prime indices.
- All composite numbers (and the number 1) MUST go to composite indices.

These are two completely independent groups. 
If we have `P` prime numbers, there are exactly `P` prime indices. The number of ways to arrange them is `P!` (P factorial).
If we have `C` composite numbers, there are `C` composite indices. The ways to arrange them is `C!` (C factorial).
Because these choices are independent, the total number of valid permutations is simply: `P! * C!`.

The Modulo Property:
Since factorials grow exponentially (100! is massive), the problem asks for the result modulo 10^9 + 7. 
To prevent integer overflow in standard languages, we apply the modulo at each step of the multiplication:
(A * B) % M = ((A % M) * (B % M)) % M
"""

# STEP 1: Define the modulo constant (10^9 + 7).
# STEP 2: Write a helper function to check if a number is prime.
# STEP 3: Count how many prime numbers exist in the range [1, n].
# STEP 4: The remaining numbers (n - primes) are composites.
# STEP 5: Write a factorial function that applies the modulo at each multiplication step.
# STEP 6: Return the product of factorial(primes) and factorial(composites), modulo 10^9 + 7.

class Solution:
    def numPrimeArrangements(self, n: int) -> int:
        
        MOD = 10**9 + 7
        
        # Step 2: Helper to check primality
        def is_prime(num: int) -> bool:
            if num < 2:
                return False
            # We only need to check up to the square root of the number
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True
            
        # Step 3 & 4: Count primes and composites
        prime_count = sum(1 for i in range(1, n + 1) if is_prime(i))
        composite_count = n - prime_count
        
        # Step 5: Custom factorial with modulo to prevent overflow
        def factorial_mod(val: int) -> int:
            result = 1
            for i in range(1, val + 1):
                result = (result * i) % MOD
            return result
            
        # Step 6: Calculate total arrangements
        total_arrangements = (factorial_mod(prime_count) * factorial_mod(composite_count)) % MOD
        
        return total_arrangements

"""
WHY EACH PART:
- is_prime(num): Uses the `num**0.5` optimization. A mathematical rule states that if a number has a divisor greater than its square root, it must also have a corresponding divisor smaller than its square root.
- factorial_mod(val): While Python handles arbitrarily large integers automatically, applying the modulo inside the loop is a fundamental competitive programming practice to keep operations within 64-bit limits for languages like C++ or Java.
- MOD = 10**9 + 7: This specific number is a large prime. Using it prevents hash collisions and guarantees safe mathematical operations across almost all data types.

HOW IT WORKS (Example: n = 5):
Count Primes:
├── is_prime(1) -> False
├── is_prime(2) -> True
├── is_prime(3) -> True
├── is_prime(4) -> False
└── is_prime(5) -> True
prime_count = 3
composite_count = 5 - 3 = 2

Calculate Factorials:
├── factorial_mod(3) = (1 * 2 * 3) % MOD = 6
└── factorial_mod(2) = (1 * 2) % MOD = 2

Final Result:
└── (6 * 2) % MOD = 12 ✓

TIME COMPLEXITY: O(N * sqrt(N)) - Finding primes takes O(sqrt(N)) for each of the N numbers. The factorial loops take O(N). Since N <= 100, this is microscopically fast.
SPACE COMPLEXITY: O(1) - Only a few integer variables are stored.

CONCEPTS USED:
- Combinatorics (Permutations & Factorials)
- Prime Number Theory
- Modular Arithmetic
"""

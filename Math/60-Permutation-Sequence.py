# 60. Permutation Sequence
# Difficulty: Hard
# https://leetcode.com/problems/permutation-sequence/

"""
PROBLEM:
The set [1, 2, 3, ..., n] contains n! unique permutations.
Given n and k, return the k-th permutation sequence (1-indexed).

EXAMPLES:
n = 3, k = 3 → "213"
All permutations of {1,2,3} in order:
1. "123"
2. "132"
3. "213" ← k=3
4. "231"
5. "312"
6. "321"

n = 4, k = 9 → "2314"
n = 3, k = 1 → "123"

CONSTRAINTS:
- 1 <= n <= 9
- 1 <= k <= n!

KEY INSIGHT:
Permutations are grouped by their first digit.
Each group has (n-1)! permutations.

For n = 4:
- Group starting with 1: permutations 1-6   (k: 1 to 6)
- Group starting with 2: permutations 7-12  (k: 7 to 12)
- Group starting with 3: permutations 13-18 (k: 13 to 18)
- Group starting with 4: permutations 19-24 (k: 19 to 24)

We can directly calculate which group k falls into,
determine the first digit, then repeat for remaining digits.

FORMULA:
For each position:
1. group_size = (remaining_digits - 1)!
2. index = k // group_size
3. digit = available_numbers[index]
4. Remove digit from available
5. k = k % group_size
"""

# STEP 1: Create list of available numbers [1, 2, ..., n]
# STEP 2: Precompute factorials [0!, 1!, 2!, ..., (n-1)!]
# STEP 3: Convert k to 0-indexed
# STEP 4: For each position, calculate which number to use
# STEP 5: Remove used number, update k, repeat

class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        
        numeros = list(range(1, n + 1))                                          # Available numbers [1,2,...,n]
        
        factorial = [1] * n                                                      # Precompute factorials
        for i in range(1, n):
            factorial[i] = factorial[i - 1] * i                                  # factorial[i] = i!
        
        k -= 1                                                                   # Convert to 0-indexed
        
        resultado = []                                                           # Build result here
        
        for i in range(n - 1, -1, -1):                                           # For each position
            indice = k // factorial[i]                                           # Which group does k fall into?
            resultado.append(str(numeros[indice]))                               # Add that digit
            numeros.pop(indice)                                                  # Remove used number
            k %= factorial[i]                                                    # Update k for next iteration
        
        return ''.join(resultado)                                                # Convert list to string

"""
WHY EACH PART:
- numeros = list(range(1, n+1)): Available digits to choose from
- factorial[i] = i!: Precompute to avoid recalculating
- k -= 1: Convert from 1-indexed to 0-indexed for easier math
- range(n-1, -1, -1): Process from most significant to least significant digit
- k // factorial[i]: Determines which "group" k falls into
- numeros[indice]: Select the digit for current position
- numeros.pop(indice): Remove used digit (can't reuse in permutation)
- k %= factorial[i]: Remaining k within the selected group

HOW IT WORKS (Example: n = 4, k = 9):

Initial:
numeros = [1, 2, 3, 4]
factorial = [1, 1, 2, 6]  (indices 0,1,2,3 = 0!,1!,2!,3!)
k = 9 - 1 = 8 (0-indexed)

Iteration 1 (i = 3):
├── group_size = factorial[3] = 6
├── indice = 8 // 6 = 1
├── digit = numeros[1] = 2
├── resultado = ['2']
├── numeros = [1, 3, 4]
└── k = 8 % 6 = 2

Iteration 2 (i = 2):
├── group_size = factorial[2] = 2
├── indice = 2 // 2 = 1
├── digit = numeros[1] = 3
├── resultado = ['2', '3']
├── numeros = [1, 4]
└── k = 2 % 2 = 0

Iteration 3 (i = 1):
├── group_size = factorial[1] = 1
├── indice = 0 // 1 = 0
├── digit = numeros[0] = 1
├── resultado = ['2', '3', '1']
├── numeros = [4]
└── k = 0 % 1 = 0

Iteration 4 (i = 0):
├── group_size = factorial[0] = 1
├── indice = 0 // 1 = 0
├── digit = numeros[0] = 4
├── resultado = ['2', '3', '1', '4']
├── numeros = []
└── k = 0 % 1 = 0

Return: "2314" ✓

KEY TECHNIQUE:
- Mathematical approach: Calculate directly without generating all permutations
- Factorial number system: k can be represented as sum of factorial coefficients
- Greedy digit selection: Each digit is determined by k // (remaining permutations)

EDGE CASES:
- n = 1, k = 1: Returns "1" ✓
- k = 1 (first): Returns "123...n" (ascending) ✓
- k = n! (last): Returns "n...321" (descending) ✓
- n = 9, k = 362880: Returns "987654321" ✓
- n = 4, k = 24: Returns "4321" ✓

TIME COMPLEXITY: O(n²) - n iterations, each with O(n) pop operation
SPACE COMPLEXITY: O(n) - Store numbers list and factorial array

Note: Can be optimized to O(n log n) using a Binary Indexed Tree
or O(n) using a linked list, but for n ≤ 9, O(n²) is sufficient.

CONCEPTS USED:
- Factorial number system
- Mathematical permutation counting
- Greedy algorithm
- Array manipulation (pop)
- 0-indexed vs 1-indexed conversion
- Direct calculation vs enumeration
"""

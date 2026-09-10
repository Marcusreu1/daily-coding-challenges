# 1830. Minimum Number of Operations to Make String Sorted
# Difficulty: Hard
# https://leetcode.com/problems/minimum-number-of-operations-to-make-string-sorted/

"""
PROBLEM:
You are given a string s (0-indexed). You are asked to perform the following operation on s until you get a sorted string:
1. Find the largest index i such that 1 <= i < s.length and s[i] < s[i - 1].
2. Find the largest index j such that i <= j < s.length and s[k] < s[i - 1] for all the characters in the block [i, j].
3. Swap s[i - 1] and s[j].
4. Reverse the suffix starting at index i.
Return the number of operations needed to make the string sorted. Since the answer can be too large, return it modulo 10^9 + 7.

EXAMPLES:
Input: s = "cba" → Output: 5
Explanation: The simulation goes as follows:
Operation 1: i=2, j=2. Swap s[1] and s[2] to get s="cab", then reverse the suffix starting at 2. Now, s="cab".
Operation 2: s="bca".
Operation 3: s="bac".
Operation 4: s="acb".
Operation 5: s="abc".

CONSTRAINTS:
- 1 <= s.length <= 3000
- s consists only of lowercase English letters.

MATH RULES (LEXICOGRAPHICAL RANK & FERMAT'S LITTLE THEOREM):
The 4-step operation described perfectly matches the standard algorithm to find the PREVIOUS lexicographical permutation of a string.
Therefore, the problem simply asks for the Lexicographical Rank of the string (i.e., how many unique permutations are strictly smaller than 's').
To find this rank:
For each character in 's' at index 'i', we count how many remaining available characters are smaller than s[i].
If we place a smaller character at position 'i', the number of permutations for the remaining characters is given by:
Permutations = L! / (f_a! * f_b! * ...) where L is the remaining length and f_k is the frequency of character k.
Because we are working under modulo 10^9 + 7, division requires multiplying by the Modular Multiplicative Inverse (calculated via Fermat's Little Theorem: x^(MOD-2) % MOD).

VISUALIZATION (s = "cba"):
Initial freq: a:1, b:1, c:1
Total combinations possible per placement calculated dynamically.

i=0, char='c': Smaller available ('a', 'b') = 2. 
  Ways = 2! / (1!*1!) * 2 = 2 * 2 = 4
i=1, char='b': Smaller available ('a') = 1.
  Ways = 1! / (1!) * 1 = 1
i=2, char='a': Smaller available = 0.
  Ways = 0
  
Total Rank = 4 + 1 + 0 = 5 operations. ✓
"""

class Solution:
    def makeStringSorted(self, s: str) -> int:
        
        MOD = 10**9 + 7
        n = len(s)
        
        # STEP 1: Precompute factorials and their modular inverses to achieve O(1) combinations retrieval
        fact = [1] * (n + 1)
        inv_fact = [1] * (n + 1)
        
        for i in range(1, n + 1):
            fact[i] = (fact[i - 1] * i) % MOD
            
        # Fermat's Little Theorem: Inverse of X mod P is X^(P-2) mod P
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        
        # Backtrack the inverse factorials mathematically: 1/(n-1)! = n * 1/n!
        for i in range(n - 1, -1, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD
            
        # STEP 2: Build the character frequency array
        freq = [0] * 26
        for char in s:
            freq[ord(char) - 97] += 1
            
        # Precompute the inverse denominator for the entire string's initial state
        denom_inv = 1
        for count in freq:
            denom_inv = (denom_inv * inv_fact[count]) % MOD
            
        total_operations = 0
        
        # STEP 3: Traverse the string and calculate permutations for smaller prefixes
        for i in range(n):
            char_idx = ord(s[i]) - 97
            
            # Sum up frequencies of all characters strictly smaller than the current one
            smaller_count = sum(freq[:char_idx])
            
            # Number of characters left to place (excluding the current position)
            rem_length = n - 1 - i
            
            # Apply the combinatorics formula: L! * (1 / product(freq!)) * smaller_chars
            ways = (fact[rem_length] * denom_inv) % MOD
            ways = (ways * smaller_count) % MOD
            
            total_operations = (total_operations + ways) % MOD
            
            # STEP 4: Update the denominator for the next iteration in O(1) time
            # Multiplying the inverse denominator by freq[char_idx] acts as dividing it by the factorial fraction seamlessly
            denom_inv = (denom_inv * freq[char_idx]) % MOD
            freq[char_idx] -= 1
            
        return total_operations

"""
WHY EACH PART:
- pow(fact[n], MOD - 2, MOD): The standard and most efficient way to compute modular inverses in competitive programming.
- inv_fact[i] = (inv_fact[i + 1] * (i + 1)): Calculating 3000 modular inverses individually with pow() is slow. We calculate the largest one and iterate backwards to generate the rest in O(N).
- denom_inv = (denom_inv * freq[char_idx]): Algebraically modifies the precomputed fraction 1/f! to become 1/(f-1)!, strictly maintaining O(1) state transitions.

KEY TECHNIQUE:
- Mathematics (Lexicographical Rank): Translating a procedural simulation into a counting problem.
- Modular Arithmetic Optimization: Bypassing modulo division limitations using cached Multiplicative Inverses.

EDGE CASES:
- String is already sorted (e.g., "abc"): 'smaller_count' evaluates to 0 on every pass. Returns 0 operations instantly.
- Maximum constraints (N=3000, all identical characters e.g., "aaa..."): Combinatorics formula safely resolves 0 remaining permutations, scaling beautifully.

TIME COMPLEXITY: O(N) - We iterate through the string once, with an inner loop slicing an array of fixed size 26. Precomputations also run strictly in O(N).
SPACE COMPLEXITY: O(N) - Storing the factorials and inverse factorials arrays requires space proportional to N.

CONCEPTS USED:
- Combinatorics
- Fermat's Little Theorem
- Prefix Accumulation
- Array state tracking
"""

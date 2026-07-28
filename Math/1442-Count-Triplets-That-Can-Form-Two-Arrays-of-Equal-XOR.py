# 1442. Count Triplets That Can Form Two Arrays of Equal XOR
# Difficulty: Medium
# https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/

"""
PROBLEM:
Given an array of integers `arr`.
We want to select three indices i, j and k where (0 <= i < j <= k < arr.length).
Let's define a and b as follows:
a = arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1]
b = arr[j] ^ arr[j + 1] ^ ... ^ arr[k]
Return the number of triplets (i, j and k) Where a == b.

EXAMPLES:
Input: arr = [2,3,1,6,7]
Output: 4
(Explanation: The triplets are (0,1,2), (0,2,2), (2,3,4) and (2,4,4)
For example, for i=0, j=1, k=2: 
a = arr[0] = 2. 
b = arr[1] ^ arr[2] = 3 ^ 1 = 2. a == b. ✓)

Input: arr = [1,1,1,1,1]
Output: 10

CONSTRAINTS:
- 1 <= arr.length <= 300
- 1 <= arr[i] <= 10^8

ALGORITHM LOGIC (XOR Properties & Prefix Hashing):
1. a == b is mathematically equivalent to a ^ b == 0.
2. Therefore, we are strictly looking for subarrays `arr[i...k]` where the total XOR is 0.
3. If a subarray `arr[i...k]` has an XOR of 0, any index `j` strictly between `i` and `k` will 
   split it into two valid halves where `a == b`.
4. How many such `j` indices exist for a valid `(i, k)` pair? Exactly `k - i`.
5. We track the running XOR (Prefix XOR). If we encounter a Prefix XOR value at index `k` 
   that we previously saw at index `i-1`, the elements between them evaluate to 0.
6. To avoid O(N^2) inner loops calculating `k - i`, we store the frequency of each prefix 
   and the sum of its previous indices in Hash Maps.
7. The number of new triplets found at `k` can be added instantly using the formula:
   (count_of_prefix_seen * k) - sum_of_previous_indices.

VISUALIZATION (arr = [2, 3, 1]):
Prefix Maps init: counts={0:1}, totals={0:0}

k=0, val=2: prefix = 0 ^ 2 = 2.
Maps update: counts={0:1, 2:1}, totals={0:0, 2:1}

k=1, val=3: prefix = 2 ^ 3 = 1.
Maps update: counts={0:1, 2:1, 1:1}, totals={..., 1:2}

k=2, val=1: prefix = 1 ^ 1 = 0.
We've seen prefix '0' before!
Triplets generated: (counts[0] * 2) - totals[0] 
Triplets = (1 * 2) - 0 = 2.
ans = 2.
(These two triplets correspond to (0,1,2) and (0,2,2)). ✓
"""

# STEP 1: Initialize result accumulator and running XOR prefix
# STEP 2: Initialize hash maps to store frequencies and index sums of prefix values
# STEP 3: Iterate through the array linearly (O(N))
# STEP 4: Apply XOR cancellation property check. If prefix exists, calculate triplets mathematically
# STEP 5: Update the state of the hash maps for future calculations

class Solution:
    def countTriplets(self, arr: list[int]) -> int:
        
        ans = 0
        prefix = 0
        
        # Hash map to track how many times a prefix XOR value has occurred
        counts = {0: 1}
        # Hash map to track the sum of the indices where a prefix XOR value occurred
        totals = {0: 0}
        
        for k, val in enumerate(arr):
            # Calculate running XOR up to current index k
            prefix ^= val
            
            # If we've seen this prefix before, the subarray between the previous occurrences 
            # and current k has an XOR of 0.
            if prefix in counts:
                # Add all combinations of j mathematically: sum of (k - i)
                ans += counts[prefix] * k - totals[prefix]
                
            # Update hash maps for the current prefix
            counts[prefix] = counts.get(prefix, 0) + 1
            totals[prefix] = totals.get(prefix, 0) + (k + 1)
            
        return ans

"""
WHY EACH PART:
- counts = {0: 1} & totals = {0: 0}: This sets the foundational mathematical base case. An empty subarray before index 0 has an XOR of 0. Without this, subarrays that sum to 0 starting from the absolute beginning of the array would be missed.
- counts[prefix] * k - totals[prefix]: This is algebraic factorization. Instead of a slow loop doing `(k - i_1) + (k - i_2)`, we factor out `k`: `k * (count) - (i_1 + i_2)`.
- totals[prefix] + (k + 1): We use `k + 1` instead of `k` because we are storing the boundary index `i` that will act as the start of the neutralizing subarray. The subarray XOR that gives 0 starts immediately AFTER the previous prefix index.

HOW IT WORKS (Example: arr = [1, 1]):
Init: counts={0:1}, totals={0:0}
k=0, val=1. prefix=1. counts[1]=1, totals[1]=1. ans=0.
k=1, val=1. prefix=0. '0' is in maps! 
ans += counts[0] * 1 - totals[0] -> (1 * 1) - 0 = 1.
Updates: counts[0]=2, totals[0]=2.
Returns ans = 1. Triplet (0, 1, 1). ✓

KEY TECHNIQUE:
- Bitwise Manipulation (XOR Cancellation Property)
- Prefix Sums (Prefix XOR)
- Hash Map State Tracking (O(N) Optimization)

EDGE CASES:
- No valid subarrays (e.g., [2, 4, 8]): The prefix will continuously grow and never match previous hash map entries. Returns 0 correctly. ✓
- Array with identical elements (e.g., [1,1,1,1]): Rapidly alternates prefixes between `1` and `0`, generating a combinatorial explosion of valid triplets flawlessly tracked by the multiplication formula. ✓

TIME COMPLEXITY: O(N) - We iterate through the array exactly once. Hash map lookups and insertions execute in O(1) average time. This is a massive optimization compared to the brute force O(N^3) or prefix-array O(N^2).
SPACE COMPLEXITY: O(N) - In the worst case, every running XOR prefix is unique, requiring O(N) space to store the key-value pairs in both Hash Maps.
"""

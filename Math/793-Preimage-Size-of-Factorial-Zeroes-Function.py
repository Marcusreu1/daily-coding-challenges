# 793. Preimage Size of Factorial Zeroes Function
# Difficulty: Hard
# https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/

"""
PROBLEM:
Let f(x) be the number of zeroes at the end of x!. Recall that x! = 1 * 2 * 3 * ... * x.
For example, f(3) = 0 because 3! = 6 has no zeroes at the end, while f(11) = 2 because 11! = 39916800 has two zeroes.
Given an integer k, return the number of non-negative integers x have the property that f(x) == k.

EXAMPLES:
Input: k = 0   → Output: 5
Explanation: 0!, 1!, 2!, 3!, and 4! all end with 0 zeroes.

Input: k = 5   → Output: 0
Explanation: There is no x such that x! ends in 5 zeroes. 
(24! has 4 zeroes, and 25! jumps to 6 zeroes).

Input: k = 3   → Output: 5

CONSTRAINTS:
- 0 <= k <= 10^9

LOGIC RULES (MATH & BINARY SEARCH):
1. Trailing zeroes are created by multiplying 10 (which is 2 * 5). Since 2s are abundant in factorials, 
   the number of trailing zeroes is strictly determined by the number of times 5 acts as a prime factor.
2. The zeroes function f(x) steps by at least 1 every 5 numbers. 
   Therefore, any valid number of zeroes 'k' will always be shared by exactly 5 consecutive numbers.
3. Because numbers like 25, 125, 625 contain multiple 5s as factors, f(x) will sometimes skip certain integers 
   (like k=5). If k is a skipped integer, 0 numbers share it.
4. Conclusion: The answer will ALWAYS be either 5 or 0.
5. Since f(x) is monotonically non-decreasing, we can find if 'k' exists using Binary Search.

VISUALIZATION (Zeroes mapping):
x:    ... 20, 21, 22, 23, 24 | 25, 26, 27, 28, 29 | 30, 31...
f(x): ...  4,  4,  4,  4,  4 |  6,  6,  6,  6,  6 |  7,  7...

Notice that f(x) = 5 is completely skipped!
If k = 4, there are 5 numbers. Return 5.
If k = 5, there are 0 numbers. Return 0.
If k = 6, there are 5 numbers. Return 5.
"""

# STEP 1: Define a helper function to count trailing zeroes in x!
# STEP 2: Set up the Binary Search range. Lowest is 0, highest is safely 5 * k.
# STEP 3: Perform standard binary search on the monotonic function f(x).
# STEP 4: If we hit exactly k, return 5 immediately.
# STEP 5: If the while loop completes without hitting k, it means k was skipped. Return 0.

class Solution:
    def preimageSizeFZF(self, k: int) -> int:
        
        # Helper function to count how many 5s are in the prime factorization of x!
        def get_zeroes(x: int) -> int:
            zeroes = 0
            while x > 0:
                zeroes += x // 5
                x //= 5
            return zeroes
            
        low = 0
        high = 5 * k
        
        while low <= high:
            mid = (low + high) // 2
            
            calculated_zeroes = get_zeroes(mid)
            
            if calculated_zeroes == k:
                return 5                                 # k exists, so there are exactly 5 integers that produce it
                
            elif calculated_zeroes < k:
                low = mid + 1                            # We need more zeroes, move search window UP
                
            else:
                high = mid - 1                           # We have too many zeroes, move search window DOWN
                
        return 0                                         # Binary search finished without finding k. It was skipped.

"""
WHY EACH PART:
- zeroes += x // 5 and x //= 5: A number like 25 contributes two 5s. 125 contributes three. 
  By dividing the number by 5 repeatedly and summing the quotients, we capture all single, double, 
  and triple powers of 5 perfectly in O(log5 N) time.
- high = 5 * k: Since every group of 5 numbers adds at least one 0, the number 'x' that produces 'k' zeroes 
  can never be larger than 5 * k. This gives us a tight upper bound for the binary search.
- return 5 / return 0: Bypasses the need to find the left and right boundaries of the matching range. 
  Because of the nature of factors of 5, the block size of identical f(x) values is always 5.

HOW IT WORKS (Example dry run for k = 5):

Initial state: low = 0, high = 25
Iteration 1:
├── mid = (0 + 25) // 2 = 12
├── get_zeroes(12) = 12 // 5 = 2. 
├── 2 < 5. We need more. low = 13.

Iteration 2:
├── mid = (13 + 25) // 2 = 19
├── get_zeroes(19) = 19 // 5 = 3.
├── 3 < 5. We need more. low = 20.

Iteration 3:
├── mid = (20 + 25) // 2 = 22
├── get_zeroes(22) = 22 // 5 = 4.
├── 4 < 5. We need more. low = 23.

Iteration 4:
├── mid = (23 + 25) // 2 = 24
├── get_zeroes(24) = 4.
├── 4 < 5. We need more. low = 25.

Iteration 5:
├── mid = (25 + 25) // 2 = 25
├── get_zeroes(25) = 25 // 5 + 5 // 5 = 5 + 1 = 6.
├── 6 > 5. We have too many. high = 24.

Exit condition met (low > high). The search failed. Returns 0. ✓

EDGE CASES:
- k = 0: low=0, high=0. mid=0. get_zeroes(0) is 0. Matches k! Returns 5. ✓
- k is very large (10^9): Binary search handles ranges of 5 * 10^9 in about 32 iterations. Instant. ✓

TIME COMPLEXITY: O(log(K) * log5(K))
Where K is the target number of zeroes. The binary search halves the search space of size 5*K, taking log2(5K) iterations. 
Inside each iteration, get_zeroes divides by 5 repeatedly, taking log5(X) operations. 
Since maximum K is 10^9, it runs in ~32 * 13 = ~400 tiny operations. Extremely fast O(1) in practical terms.

SPACE COMPLEXITY: O(1)
Only integer variables (`low`, `high`, `mid`, `calculated_zeroes`) are used. Memory is strictly constant.
"""

"""
564. Find the Closest Palindrome
Difficulty: Hard
https://leetcode.com/problems/find-the-closest-palindrome/

PROBLEM:
    Given a string n representing an integer, return the closest
    integer (not including itself) which is a palindrome.
    If there is a tie, return the smaller one.
    "Closest" is measured in absolute difference.

EXAMPLES:
    Input: n = "123"   → Output: "121"
    Input: n = "1"     → Output: "0"
    Input: n = "100"   → Output: "99"
    Input: n = "11911" → Output: "11811"

CONSTRAINTS:
    1 <= n.length <= 18
    n does not have leading zeros
    n represents an integer in [1, 10^18]

KEY INSIGHT:
    Only 5 candidates can possibly be the answer:
        1. Mirror prefix as-is        → same-length palindrome
        2. Mirror (prefix + 1)        → next same-length palindrome
        3. Mirror (prefix - 1)        → prev same-length palindrome
        4. 10^(d-1) - 1               → largest palindrome with fewer digits (999...9)
        5. 10^d + 1                   → smallest palindrome with more digits (100...01)

    Generate all 5, exclude n itself, pick closest (smaller on tie).

CHALLENGES:
    Many edge cases (powers of 10, single digit, all 9s, already palindrome)
    Prefix ± 1 can change number of digits
    Tie-breaking rule (pick the smaller)
    Correctly mirroring for odd vs even length numbers

SOLUTION:
    Extract prefix (first half), generate 5 candidates by mirroring
    prefix-1, prefix, prefix+1, and the two boundary palindromes.
    Compare all candidates to find the closest.
"""


# STEP 1: Define helper to build palindrome from a prefix
# STEP 2: Extract prefix from n
# STEP 3: Generate 5 candidates
# STEP 4: Remove n itself from candidates
# STEP 5: Find candidate with minimum |candidate - n|, smaller on tie


class Solution:
    def nearestPalindromic(self, n: str) -> str:

        d = len(n)                                                    # Number of digits
        num = int(n)                                                  # Numeric value of n

        candidates = set()                                            # Use set to avoid duplicates

        # --- Candidate 4 & 5: boundary palindromes ---
        candidates.add(10 ** (d - 1) - 1)                            # 999...9 (d-1 digits), e.g., 99 for d=3
        candidates.add(10 ** d + 1)                                   # 100...01 (d+1 digits), e.g., 1001 for d=3

        # --- Candidates 1, 2, 3: mirror prefix, prefix±1 ---
        prefix = int(n[:(d + 1) // 2])                               # First ⌈d/2⌉ digits as integer

        for p in [prefix - 1, prefix, prefix + 1]:                   # Try prefix-1, prefix, prefix+1
            p_str = str(p)                                            # Convert to string for mirroring
            if d % 2 == 1:                                            # Odd length: mirror without center
                palindrome = p_str + p_str[:-1][::-1]                 # "123" → "123" + "12"[::-1] = "12321"
            else:                                                     # Even length: mirror fully
                palindrome = p_str + p_str[::-1]                      # "12" → "12" + "21" = "1221"
            candidates.add(int(palindrome))                           # Add to candidate set

        candidates.discard(num)                                       # Remove n itself (answer must differ)

        closest = None                                                # Track best candidate

        for c in candidates:                                          # Check each candidate
            if closest is None:                                       # First candidate
                closest = c
            elif abs(c - num) < abs(closest - num):                   # Closer than current best
                closest = c
            elif abs(c - num) == abs(closest - num) and c < closest:  # Same distance, pick smaller
                closest = c

        return str(closest)                                           # Return as string


"""
WHY EACH PART:
    d = len(n):              Number of digits determines prefix length and boundary candidates
    candidates = set():      Avoids checking duplicate candidates
    10^(d-1) - 1:            Covers "drop a digit" case (e.g., 100 → 99)
    10^d + 1:                Covers "add a digit" case (e.g., 999 → 1001)
    (d+1) // 2:              Ceiling division — includes the center digit for odd lengths
    prefix ± 1:              Generates neighboring palindromes of same length
    d % 2 == 1 check:        Odd/even lengths mirror differently
    p_str + p_str[:-1][::-1]: Odd: "123" → "12321" (don't repeat center)
    p_str + p_str[::-1]:      Even: "12" → "1221" (mirror fully)
    discard(num):            Answer can't be n itself
    tie-breaking (c < closest): Problem requires smaller palindrome on tie


HOW IT WORKS (Example: n = "123"):

    d = 3, num = 123
    prefix = int("12") → wait, (3+1)//2 = 2 → n[:2] = "12" → prefix = 12

    Boundary candidates:
    ├── 10^2 - 1 = 99
    └── 10^3 + 1 = 1001

    Mirror candidates (d=3, odd):
    ├── prefix-1 = 11 → "11" + "1"[::-1] = "111"  → 111
    ├── prefix   = 12 → "12" + "1"[::-1] = "121"  → 121
    └── prefix+1 = 13 → "13" + "1"[::-1] = "131"  → 131

    Candidates = {99, 1001, 111, 121, 131}
    Remove 123? Not present.

    Distances:
    ├── |123-99|   = 24
    ├── |123-1001| = 878
    ├── |123-111|  = 12
    ├── |123-121|  = 2    ← MINIMUM 
    └── |123-131|  = 8

    return "121" 


HOW IT WORKS (Example: n = "100"):

    d = 3, num = 100
    prefix = int("10") = 10   (n[:2] = "10")

    Boundary candidates:
    ├── 10^2 - 1 = 99
    └── 10^3 + 1 = 1001

    Mirror candidates (d=3, odd):
    ├── prefix-1 = 9  → "9" + ""[::-1] = "9"    → 9
    ├── prefix   = 10 → "10" + "1"[::-1] = "101" → 101
    └── prefix+1 = 11 → "11" + "1"[::-1] = "111" → 111

    Candidates = {99, 1001, 9, 101, 111}
    Remove 100? Not present.

    Distances:
    ├── |100-99|   = 1    ← TIE
    ├── |100-101|  = 1    ← TIE
    ├── |100-1001| = 901
    ├── |100-9|    = 91
    └── |100-111|  = 11

    Tie between 99 and 101 → pick smaller → "99" 


HOW IT WORKS (Example: n = "1"):

    d = 1, num = 1
    prefix = int("1") = 1

    Boundary candidates:
    ├── 10^0 - 1 = 0
    └── 10^1 + 1 = 11

    Mirror candidates (d=1, odd):
    ├── prefix-1 = 0 → "0" + ""[::-1] = "0"  → 0
    ├── prefix   = 1 → "1" + ""[::-1] = "1"  → 1
    └── prefix+1 = 2 → "2" + ""[::-1] = "2"  → 2

    Candidates = {0, 11, 2} (1 discarded = itself)

    Distances:
    ├── |1-0|  = 1  ← MINIMUM 
    ├── |1-11| = 10
    └── |1-2|  = 1  ← TIE

    Tie between 0 and 2 → pick smaller → "0" 


HOW IT WORKS (Example: n = "11911"):

    d = 5, num = 11911
    prefix = int("119") = 119

    Boundary candidates:
    ├── 10^4 - 1 = 9999
    └── 10^5 + 1 = 100001

    Mirror candidates (d=5, odd):
    ├── prefix-1 = 118 → "118" + "11"[::-1] = "11811"  → 11811
    ├── prefix   = 119 → "119" + "11"[::-1] = "11911"  → 11911
    └── prefix+1 = 120 → "120" + "12"[::-1] = "12021"  → 12021

    Candidates = {9999, 100001, 11811, 12021} (11911 discarded)

    Distances:
    ├── |11911-9999|   = 1912
    ├── |11911-100001| = 88090
    ├── |11911-11811|  = 100   ← MINIMUM 
    └── |11911-12021|  = 110

    return "11811" 


WHY ONLY 5 CANDIDATES ARE ENOUGH:
    Among palindromes with SAME number of digits:
        They are determined by their first half (prefix).
        The closest palindromes must have prefix = original prefix,
        prefix+1, or prefix-1. Anything further is guaranteed farther.

        Proof: If palindrome P has prefix = original_prefix + 2,
        then palindrome with prefix+1 is BETWEEN n and P,
        so P can't be the closest. ✓

    Among palindromes with DIFFERENT number of digits:
        The closest possible are:
        - Largest with fewer digits: 999...9 = 10^(d-1) - 1
        - Smallest with more digits: 100...01 = 10^d + 1
        
        Any other different-length palindrome is further away.


WHY ODD/EVEN MIRRORING DIFFERS:
    Odd length (d=5):  "12345"
        prefix = "123" (3 digits, includes center)
        mirror = "123" + reverse("12") = "12321"
                          ↑ exclude center to avoid duplication
    
    Even length (d=4): "1234"
        prefix = "12" (2 digits)
        mirror = "12" + reverse("12") = "1221"
                          ↑ mirror all of prefix


HANDLING SPECIAL CASES:
    n = "1":              Boundary 10^0-1=0 catches it → "0" ✓
    n = "10":             Boundary 10^1-1=9 catches it → "9" ✓
    n = "99":             prefix+1=10 → "1001", boundary handles it ✓
    n = "11":             prefix-1=0 → "0", prefix+1=2 → "22" → "9" wins ✓
    Already palindrome:   Discarded, prefix±1 provides alternatives ✓
    All 9s "999":         prefix+1=10 → "1001", boundary 10^2-1=99 ✓
    Power of 10 "1000":   Boundary 10^3-1=999 handles it ✓


KEY TECHNIQUE:
    Candidate generation:    Only 5 candidates needed (not brute force)
    Palindrome mirroring:    Build from first half, copy to second half
    Boundary palindromes:    Handle digit-count changes (999, 1001)
    Set for deduplication:   Avoid checking same candidate twice
    Tie-breaking logic:      Pick smaller when equidistant


EDGE CASES:
    n = "1":                "0" ✓
    n = "10":               "9" ✓
    n = "99":               "101" ✓
    n = "100":              "99" ✓
    n = "999":              "1001" ✓
    n = "1000":             "999" ✓
    n = "11":               "9" ✓
    n = "12321" (palindrome): "12221" ✓
    n = "1000000000000000000" (10^18): Handles large numbers ✓


TIME COMPLEXITY: O(d)
    d = number of digits in n (at most 18)
    Generating each candidate: O(d) for string operations
    5 candidates × O(d) = O(d)

SPACE COMPLEXITY: O(d)
    String representations of candidates
    Set with at most 5 elements


CONCEPTS USED:
    Palindrome construction (mirroring)
    Candidate generation (bounded search space)
    Prefix manipulation (first half determines palindrome)
    Boundary analysis (digit count changes)
    Tie-breaking comparison
    Set for deduplication
"""

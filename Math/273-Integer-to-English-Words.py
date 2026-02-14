# 273. Integer to English Words
# Difficulty: Hard
# https://leetcode.com/problems/integer-to-english-words/

"""
PROBLEM:
Convert a non-negative integer num to its English words representation.

EXAMPLES:
Input: num = 123        → Output: "One Hundred Twenty Three"
Input: num = 12345      → Output: "Twelve Thousand Three Hundred Forty Five"
Input: num = 1234567    → Output: "One Million Two Hundred Thirty Four Thousand 
                                   Five Hundred Sixty Seven"
Input: num = 0          → Output: "Zero"

CONSTRAINTS:
- 0 <= num <= 2³¹ - 1 (max is about 2.1 billion)

KEY INSIGHT:
English numbers are grouped in blocks of 3 digits with scales:
Billion (10⁹), Million (10⁶), Thousand (10³), and base.

Process each 3-digit block separately, then combine with scale names.

CHALLENGES:
1. "Teens" (10-19) have irregular names
2. Skip blocks that are zero (1000000 → "One Million", not "...Zero Thousand...")
3. Handle spacing correctly

SOLUTION:
1. Define lookup tables for ones, teens, tens
2. Create helper to convert any number < 1000 to words
3. Process from largest scale (Billion) down to base
4. Combine all parts with proper spacing
"""

# STEP 1: Define word lookup tables
# STEP 2: Create helper function for numbers < 1000
# STEP 3: Process each scale (Billion, Million, Thousand, base)
# STEP 4: Combine and return result

class Solution:
    def numberToWords(self, num: int) -> str:
        
        if num == 0:                                                             # Special case
            return "Zero"
        
        # Lookup tables
        ones = ["", "One", "Two", "Three", "Four", "Five", 
                "Six", "Seven", "Eight", "Nine"]
        
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", 
                 "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", 
                "Sixty", "Seventy", "Eighty", "Ninety"]
        
        def helper(n: int) -> str:
            """Convert number < 1000 to English words."""
            if n == 0:
                return ""
            elif n < 10:
                return ones[n]
            elif n < 20:
                return teens[n - 10]
            elif n < 100:
                return tens[n // 10] + (" " + ones[n % 10] if n % 10 else "")
            else:  # n < 1000
                return ones[n // 100] + " Hundred" + (" " + helper(n % 100) if n % 100 else "")
        
        # Scales: (value, name)
        scales = [
            (1_000_000_000, "Billion"),
            (1_000_000, "Million"),
            (1_000, "Thousand"),
            (1, "")                                                              # Base (no suffix)
        ]
        
        result = []
        
        for value, name in scales:
            if num >= value:                                                     # If this scale applies
                quotient = num // value
                num %= value                                                     # Remaining for next scale
                
                part = helper(quotient)                                          # Convert this block
                if name:
                    part += " " + name                                           # Add scale name
                result.append(part)
        
        return " ".join(result)


"""
WHY EACH PART:
- num == 0: Only case where we return "Zero"; otherwise 0 blocks are skipped
- ones[]: Words for 1-9 (index 0 is empty string for convenience)
- teens[]: Special words for 10-19 (irregular in English)
- tens[]: Words for 20, 30, ..., 90 (indices 0,1 unused)
- helper(n): Recursively converts any n < 1000 to words
- n < 10: Simple ones lookup
- n < 20: Teens lookup (n-10 gives index 0-9)
- n < 100: Tens word + optional ones word
- n < 1000: Hundreds + recursive call for remainder
- scales[]: List of (value, name) from largest to smallest
- num >= value: Check if this scale contributes
- quotient = num // value: How many of this scale
- num %= value: Reduce num for next iteration
- result.append(part): Collect non-empty parts
- " ".join(result): Combine with single spaces

HOW IT WORKS (Example: num = 12345):

┌─ Initial ─────────────────────────────────────────────────┐
│  num = 12345                                              │
│  scales = [(10⁹,"Billion"), (10⁶,"Million"),             │
│            (10³,"Thousand"), (1,"")]                      │
└───────────────────────────────────────────────────────────┘

┌─ Scale: Billion (10⁹) ────────────────────────────────────┐
│  12345 >= 10⁹? No → skip                                  │
└───────────────────────────────────────────────────────────┘

┌─ Scale: Million (10⁶) ────────────────────────────────────┐
│  12345 >= 10⁶? No → skip                                  │
└───────────────────────────────────────────────────────────┘

┌─ Scale: Thousand (10³) ───────────────────────────────────┐
│  12345 >= 1000? Yes                                       │
│  quotient = 12345 // 1000 = 12                            │
│  num = 12345 % 1000 = 345                                 │
│                                                           │
│  helper(12):                                              │
│    12 < 20 → teens[12-10] = teens[2] = "Twelve"          │
│                                                           │
│  part = "Twelve" + " " + "Thousand" = "Twelve Thousand"  │
│  result = ["Twelve Thousand"]                            │
└───────────────────────────────────────────────────────────┘

┌─ Scale: Base (1) ─────────────────────────────────────────┐
│  345 >= 1? Yes                                            │
│  quotient = 345                                           │
│  num = 0                                                  │
│                                                           │
│  helper(345):                                             │
│    345 >= 100 → ones[3] = "Three"                        │
│    "Three Hundred" + " " + helper(45)                    │
│                                                           │
│    helper(45):                                            │
│      45 >= 20 → tens[4] = "Forty"                        │
│      "Forty" + " " + ones[5] = "Forty Five"              │
│                                                           │
│    = "Three Hundred Forty Five"                          │
│                                                           │
│  part = "Three Hundred Forty Five" (no scale name)       │
│  result = ["Twelve Thousand", "Three Hundred Forty Five"]│
└───────────────────────────────────────────────────────────┘

┌─ Final ───────────────────────────────────────────────────┐
│  " ".join(result)                                         │
│  = "Twelve Thousand Three Hundred Forty Five" ✓          │
└───────────────────────────────────────────────────────────┘

HOW HELPER WORKS (Converting 3-digit blocks):

┌────────────────────────────────────────────────────────────┐
│  helper(n) handles 0-999:                                  │
│                                                            │
│  n = 0:    return ""        (skip zeros)                  │
│  n = 5:    return "Five"    (ones)                        │
│  n = 15:   return "Fifteen" (teens)                       │
│  n = 50:   return "Fifty"   (tens only)                   │
│  n = 55:   return "Fifty Five"  (tens + ones)             │
│  n = 100:  return "One Hundred" (hundreds only)           │
│  n = 115:  return "One Hundred Fifteen"                   │
│  n = 155:  return "One Hundred Fifty Five"                │
└────────────────────────────────────────────────────────────┘

HANDLING EDGE CASES:

┌─ num = 0 ─────────────────────────────────────────────────┐
│  Special case at start → return "Zero"                    │
│  This is the ONLY time "Zero" appears in output           │
└───────────────────────────────────────────────────────────┘

┌─ num = 1000000 (One Million) ─────────────────────────────┐
│  Million scale: 1000000 // 10⁶ = 1 → helper(1) = "One"   │
│  part = "One Million"                                     │
│  num = 0, remaining scales don't add anything            │
│  result = ["One Million"]                                │
│  Output: "One Million" ✓ (no "Zero Thousand Zero")       │
└───────────────────────────────────────────────────────────┘

┌─ num = 1000010 (One Million Ten) ─────────────────────────┐
│  Million: "One Million"                                   │
│  Thousand: 1000010 % 10⁶ = 10, 10 // 1000 = 0 → skip    │
│  Base: 10 → helper(10) = "Ten"                           │
│  Output: "One Million Ten" ✓                             │
└───────────────────────────────────────────────────────────┘

EDGE CASES:
- num = 0: "Zero" ✓
- num = 1: "One" ✓
- num = 10: "Ten" ✓
- num = 100: "One Hundred" ✓
- num = 1000: "One Thousand" ✓
- num = 1000000: "One Million" ✓
- num = 1000000000: "One Billion" ✓
- num = 2147483647: Max int, handled correctly ✓
- num = 101: "One Hundred One" (no "and") ✓
- num = 1001: "One Thousand One" ✓

VERIFICATION TABLE:
┌─────────────────┬────────────────────────────────────────────┐
│      num        │                  Output                    │
├─────────────────┼────────────────────────────────────────────┤
│       0         │  "Zero"                                    │
│       1         │  "One"                                     │
│      12         │  "Twelve"                                  │
│      20         │  "Twenty"                                  │
│      21         │  "Twenty One"                              │
│     100         │  "One Hundred"                             │
│     123         │  "One Hundred Twenty Three"                │
│    1000         │  "One Thousand"                            │
│   12345         │  "Twelve Thousand Three Hundred Forty Five"│
│  1000000        │  "One Million"                             │
│  1000001        │  "One Million One"                         │
└─────────────────┴────────────────────────────────────────────┘

TIME COMPLEXITY: O(1)
- Maximum number has ~10 digits
- Each digit processed constant times
- Fixed number of scales (4)

SPACE COMPLEXITY: O(1)
- Fixed-size lookup tables
- Output string length bounded by max int

CONCEPTS USED:
- Divide and conquer (process blocks separately)
- Lookup tables for word mappings
- Recursion for 3-digit blocks
- Integer division and modulo for digit extraction
- String building and joining
"""

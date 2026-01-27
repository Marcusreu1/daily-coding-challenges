# 166. Fraction to Recurring Decimal
# Difficulty: Medium
# https://leetcode.com/problems/fraction-to-recurring-decimal/

"""
PROBLEM:
Given two integers representing the numerator and denominator of a fraction,
return the fraction in string format. If the fractional part is repeating,
enclose the repeating part in parentheses.

EXAMPLES:
Input: numerator = 1, denominator = 2   → Output: "0.5"
Input: numerator = 2, denominator = 1   → Output: "2"
Input: numerator = 4, denominator = 333 → Output: "0.(012)"
Input: numerator = 1, denominator = 6   → Output: "0.1(6)"

CONSTRAINTS:
- -2^31 <= numerator, denominator <= 2^31 - 1
- denominator != 0

KEY INSIGHT:
Simulate long division! If a REMAINDER repeats, the digits will repeat
from that point. Use a dictionary to track {remainder: position}.

CHALLENGES:
1. Handling negative numbers (only one negative = negative result)
2. Detecting WHERE the cycle starts (not just IF it exists)
3. Inserting parentheses at the correct position

SOLUTION:
- Handle sign separately
- Compute integer part
- Simulate long division for decimal part
- Track remainders and their positions
- When remainder repeats → insert parentheses at stored position
"""

# STEP 1: Handle edge case (numerator = 0) and determine sign
# STEP 2: Compute integer part using floor division
# STEP 3: If no remainder, return integer part only
# STEP 4: Simulate long division, tracking remainders
# STEP 5: If remainder repeats, insert parentheses and return

class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        
        if numerator == 0:                                                       # Edge case: 0/n = "0"
            return "0"
        
        result = []
        
        # STEP 1: Determine sign
        if (numerator < 0) ^ (denominator < 0):                                  # XOR: only one is negative
            result.append("-")
        
        # Work with absolute values from now on
        numerator = abs(numerator)
        denominator = abs(denominator)
        
        # STEP 2: Integer part
        integer_part = numerator // denominator
        result.append(str(integer_part))
        
        # STEP 3: Check if division is exact
        remainder = numerator % denominator
        
        if remainder == 0:                                                       # No decimal part
            return "".join(result)
        
        # STEP 4: Decimal part with long division
        result.append(".")
        
        decimal_part = []                                                        # Build decimal digits separately
        remainder_positions = {}                                                 # {remainder: index in decimal_part}
        
        while remainder != 0:                                                    # Continue until exact or cycle
            
            if remainder in remainder_positions:                                 # Cycle detected!
                cycle_start = remainder_positions[remainder]
                # Insert parentheses around repeating part
                decimal_part.insert(cycle_start, "(")
                decimal_part.append(")")
                break
            
            remainder_positions[remainder] = len(decimal_part)                   # Store position of this remainder
            
            remainder *= 10                                                      # Bring down a zero
            digit = remainder // denominator                                     # Next decimal digit
            decimal_part.append(str(digit))
            
            remainder = remainder % denominator                                  # Update remainder
        
        result.append("".join(decimal_part))
        
        return "".join(result)


"""
WHY EACH PART:
- numerator == 0: Edge case, 0 divided by anything is "0"
- XOR for sign: True only when exactly one is negative
- abs(): Work with positives, handle sign separately
- integer_part: The part before the decimal point
- remainder == 0 check: If exact division, no decimal needed
- decimal_part list: Easier to insert "(" at specific position
- remainder_positions dict: Maps remainder → position in decimal string
- remainder in dict: If seen before, cycle detected!
- cycle_start: Position where repeating pattern begins
- remainder *= 10: Simulates "bringing down a zero" in long division
- digit = remainder // denominator: Get next decimal digit
- remainder % denominator: New remainder for next iteration

HOW IT WORKS (Example: numerator=1, denominator=6):

SETUP:
├── 1 > 0 and 6 > 0 → no negative sign
├── integer_part = 1 // 6 = 0
├── remainder = 1 % 6 = 1 (not zero, continue)
└── result so far: ["0", "."]

LONG DIVISION:
┌─────────────────────────────────────────────────────────────┐
│ Iter 1:                                                     │
│ ├── remainder = 1 not in {} → store {1: 0}                  │
│ ├── remainder = 1 * 10 = 10                                 │
│ ├── digit = 10 // 6 = 1                                     │
│ ├── decimal_part = ["1"]                                    │
│ └── remainder = 10 % 6 = 4                                  │
│                                                             │
│ Iter 2:                                                     │
│ ├── remainder = 4 not in {1:0} → store {1:0, 4:1}           │
│ ├── remainder = 4 * 10 = 40                                 │
│ ├── digit = 40 // 6 = 6                                     │
│ ├── decimal_part = ["1", "6"]                               │
│ └── remainder = 40 % 6 = 4                                  │
│                                                             │
│ Iter 3:                                                     │
│ ├── remainder = 4 IS in {1:0, 4:1}! → cycle_start = 1       │
│ ├── Insert "(" at position 1: ["1", "(", "6"]               │
│ ├── Append ")": ["1", "(", "6", ")"]                        │
│ └── BREAK                                                   │
└─────────────────────────────────────────────────────────────┘

FINAL:
├── decimal_part = ["1", "(", "6", ")"]
├── result = ["0", ".", "1", "(", "6", ")"]
└── return "0.1(6)" ✓

WHY TRACK REMAINDER POSITION:
┌─────────────────────────────────────────────────────────────┐
│  4/333 = 0.012012012...                                     │
│                                                             │
│  Remainders: 4 → 40 → 67 → 4 (repeat!)                      │
│  Positions:  0    1    2                                    │
│                                                             │
│  When 4 repeats, we know cycle starts at position 0         │
│  So we get "0.(012)" not "0.0(12)" or "0.01(2)"            │
└─────────────────────────────────────────────────────────────┘

WHY XOR FOR SIGN:
┌─────────────────────────────────────────────────────────────┐
│  (a < 0) ^ (b < 0)   →   True if exactly ONE is negative    │
│                                                             │
│  -1, 2  →  True ^ False  = True   → negative result         │
│   1,-2  →  False ^ True  = True   → negative result         │
│  -1,-2  →  True ^ True   = False  → positive result         │
│   1, 2  →  False ^ False = False  → positive result         │
└─────────────────────────────────────────────────────────────┘

LONG DIVISION VISUAL:
        0.1 6 6 6...
       ┌────────────
    6  │ 1.0 0 0 0
          6
         ───
          4 0      ← remainder 4, position 1
          3 6
          ───
            4 0    ← remainder 4 again! cycle at position 1
            
Result: 0.1(6)

EDGE CASES:
- numerator = 0: Returns "0" ✓
- Exact division (4/2): Returns "2" (no decimal) ✓
- Negative result (-1/2): Returns "-0.5" ✓
- Both negative (-1/-2): Returns "0.5" ✓
- Long repeating cycle (1/97): Handles correctly ✓
- No cycle (1/8 = 0.125): Returns "0.125" ✓

TIME COMPLEXITY: O(d)
- d = denominator (maximum unique remainders)
- Remainders range from 0 to denominator-1
- Each remainder processed at most once before cycle detected

SPACE COMPLEXITY: O(d)
- Dictionary stores at most d remainders
- Result string length proportional to cycle length

CONCEPTS USED:
- Long division simulation
- Cycle detection with hash map
- XOR for sign determination
- Remainder tracking
- String building with list (efficient concatenation)
"""

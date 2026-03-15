"""
423. Reconstruct Original Digits from English
Difficulty: Medium
https://leetcode.com/problems/reconstruct-original-digits-from-english/

PROBLEM:
Given a string s containing an out-of-order English representation of
digits 0-9, return the digits in ASCENDING order.

The input is guaranteed to be valid (always maps to a set of digits).

EXAMPLES:
Input: s = "owoztneoer"  → Output: "012"  (zero + one + two)
Input: s = "fviefuro"    → Output: "45"   (four + five)

CONSTRAINTS:
    1 <= s.length <= 10^5
    s[i] is one of: 'a'-'z'
    s is guaranteed to be valid

KEY INSIGHT:
Some letters are UNIQUE to specific digit words:
    'z' → only in "zero"     'x' → only in "six"
    'w' → only in "two"      'g' → only in "eight"
    'u' → only in "four"

After counting those digits, other letters become unique:
    'o' → "one" (after removing zero, two, four)
    'h' → "three" (after removing eight)
    'f' → "five" (after removing four)
    's' → "seven" (after removing six)
    'i' → "nine" (after removing five, six, eight)

CHALLENGES:
    Letters are completely shuffled
    Multiple digits share the same letters
    Need a systematic detection order

SOLUTION:
    1. Count frequency of each letter
    2. Round 1: Detect digits with unique letters (0,2,4,6,8)
    3. Round 2: Detect digits with now-unique letters (1,3,5,7)
    4. Round 3: Detect remaining digit (9)
    5. Build result string in ascending order
"""

# STEP 1: Count letter frequencies
# STEP 2: Calculate count of each digit using unique letter formulas
# STEP 3: Build result string in ascending order

from collections import Counter

class Solution:
    def originalDigits(self, s: str) -> str:

        freq = Counter(s)                                                # Count every letter

        count = [0] * 10                                                 # count[d] = how many of digit d

        # ROUND 1: Digits with directly unique letters
        count[0] = freq['z']                                             # 'z' only in "zero"
        count[2] = freq['w']                                             # 'w' only in "two"
        count[4] = freq['u']                                             # 'u' only in "four"
        count[6] = freq['x']                                             # 'x' only in "six"
        count[8] = freq['g']                                             # 'g' only in "eight"

        # ROUND 2: Unique after subtracting round 1
        count[1] = freq['o'] - count[0] - count[2] - count[4]           # 'o' in zero, one, two, four
        count[3] = freq['h'] - count[8]                                  # 'h' in three, eight
        count[5] = freq['f'] - count[4]                                  # 'f' in four, five
        count[7] = freq['s'] - count[6]                                  # 's' in six, seven

        # ROUND 3: Remaining digit
        count[9] = freq['i'] - count[5] - count[6] - count[8]           # 'i' in five, six, eight, nine

        result = ""                                                      # Build ascending result
        for d in range(10):                                              # 0 through 9 in order
            result += str(d) * count[d]                                  # Repeat digit by its count

        return result

"""
WHY EACH PART:

    freq = Counter(s): Count all letters in one pass O(n)
    count = [0] * 10: Array indexed 0-9, one slot per digit
    count[0] = freq['z']: Only "zero" has 'z', so z-count = zero-count
    count[2] = freq['w']: Only "two" has 'w'
    count[4] = freq['u']: Only "four" has 'u'
    count[6] = freq['x']: Only "six" has 'x'
    count[8] = freq['g']: Only "eight" has 'g'
    count[1] = freq['o'] - ...: 'o' appears in zero/one/two/four, subtract known
    count[3] = freq['h'] - count[8]: 'h' appears in three/eight
    count[5] = freq['f'] - count[4]: 'f' appears in four/five
    count[7] = freq['s'] - count[6]: 's' appears in six/seven
    count[9] = freq['i'] - ...: 'i' appears in five/six/eight/nine
    str(d) * count[d]: Repeat digit string by count ("3" * 2 = "33")

HOW IT WORKS (Example: s = "fviefuro"):

    freq = {f:2, v:1, i:1, e:1, u:1, r:1, o:1}

    ROUND 1:
    ├── count[0] = freq['z'] = 0
    ├── count[2] = freq['w'] = 0
    ├── count[4] = freq['u'] = 1    ← one "four"!
    ├── count[6] = freq['x'] = 0
    └── count[8] = freq['g'] = 0

    ROUND 2:
    ├── count[1] = freq['o'] - 0 - 0 - 1 = 1 - 1 = 0
    ├── count[3] = freq['h'] - 0 = 0
    ├── count[5] = freq['f'] - 1 = 2 - 1 = 1    ← one "five"!
    └── count[7] = freq['s'] - 0 = 0

    ROUND 3:
    └── count[9] = freq['i'] - 1 - 0 - 0 = 1 - 1 = 0

    count = [0,0,0,0,1,1,0,0,0,0]
    Result: "4" * 1 + "5" * 1 = "45" ✓

WHY THIS DETECTION ORDER WORKS:

    The key is DEPENDENCY CHAINS:

    Round 1 (no dependencies):
    ├── 0: 'z' is unique → count directly
    ├── 2: 'w' is unique → count directly
    ├── 4: 'u' is unique → count directly
    ├── 6: 'x' is unique → count directly
    └── 8: 'g' is unique → count directly

    Round 2 (depends on round 1):
    ├── 1: 'o' shared with 0,2,4 → subtract them
    ├── 3: 'h' shared with 8 → subtract it
    ├── 5: 'f' shared with 4 → subtract it
    └── 7: 's' shared with 6 → subtract it

    Round 3 (depends on rounds 1+2):
    └── 9: 'i' shared with 5,6,8 → subtract them

LETTER OVERLAP TABLE:

    Letter:  Words containing it:     Used to detect:
    'z'      zero                     → 0 (round 1)
    'w'      two                      → 2 (round 1)
    'u'      four                     → 4 (round 1)
    'x'      six                      → 6 (round 1)
    'g'      eight                    → 8 (round 1)
    'o'      zero, one, two, four     → 1 (round 2)
    'h'      three, eight             → 3 (round 2)
    'f'      four, five              → 5 (round 2)
    's'      six, seven              → 7 (round 2)
    'i'      five, six, eight, nine  → 9 (round 3)

WHY ASCENDING ORDER IS AUTOMATIC:

    for d in range(10):              # 0, 1, 2, ..., 9
        result += str(d) * count[d]  # adds 0s, then 1s, then 2s...

    Example: count = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    └── "0"*1 + "1"*1 + "2"*1 = "012" ✓ (already ascending)

EDGE CASES:

    Single digit "zroe": freq has z→"zero" → "0" ✓
    All same digit "zerozero": count[0]=2 → "00" ✓
    All ten digits present: Each counted correctly ✓
    Large input (10^5 chars): O(n) handles it ✓
    Letters only from one digit: Only that count > 0 ✓

TIME COMPLEXITY: O(n)
    O(n) to count letter frequencies
    O(1) to compute 10 digit counts (fixed formulas)
    O(n) to build result string (total digits ≤ n)

SPACE COMPLEXITY: O(1)
    freq has at most 26 keys (alphabet)
    count has fixed size 10
    (result string excluded as it's the output)

CONCEPTS USED:
    Frequency counting (Counter / HashMap)
    Unique identifier detection
    Dependency-ordered elimination (round 1 → 2 → 3)
    Set theory (letter overlap analysis)
    String multiplication for result building
"""

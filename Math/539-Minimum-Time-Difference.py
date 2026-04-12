"""
539. Minimum Time Difference
Difficulty: Medium
https://leetcode.com/problems/minimum-time-difference/

PROBLEM:
    Given a list of 24-hour clock time points in "HH:MM" format,
    return the minimum difference in minutes between any two time points.

EXAMPLES:
    Input: timePoints = ["23:59","00:00"]        → Output: 1
    Input: timePoints = ["00:00","23:59","00:00"] → Output: 0
    Input: timePoints = ["05:31","22:08","00:35"] → Output: 147

CONSTRAINTS:
    2 <= timePoints.length <= 2 × 10^4
    Each timePoint is in "HH:MM" format

KEY INSIGHT:
    Convert all times to minutes [0..1439].
    Sort them. Minimum difference must be between ADJACENT times.
    Don't forget the CIRCULAR case: last → first (wrapping midnight).

    Also: if len > 1440, by Pigeonhole Principle, two times are
    identical → answer is 0.

CHALLENGES:
    The clock is CIRCULAR (23:59 and 00:00 are 1 minute apart)
    Handling the wrap-around case (last element vs first element)
    Recognizing the Pigeonhole optimization

SOLUTION:
    Convert "HH:MM" → minutes
    Sort the array
    Compare all consecutive pairs + the circular pair
    Return the minimum difference
"""


# STEP 1: Pigeonhole check (more times than minutes in a day)
# STEP 2: Convert all time strings to total minutes
# STEP 3: Sort the minutes array
# STEP 4: Compare all adjacent pairs for minimum difference
# STEP 5: Compare circular pair (last and first wrapping around midnight)
# STEP 6: Return overall minimum


class Solution:
    def findMinDifference(self, timePoints: List[str]) -> int:

        if len(timePoints) > 1440:                                    # Pigeonhole: must have duplicates
            return 0

        minutes = []                                                  # Store all times as total minutes

        for tp in timePoints:                                         # Convert each "HH:MM" to minutes
            h, m = map(int, tp.split(":"))                            # Split and parse hours and minutes
            minutes.append(h * 60 + m)                                # Total minutes since 00:00

        minutes.sort()                                                # Sort to compare adjacent pairs

        min_diff = float("inf")                                       # Track minimum difference found

        for i in range(1, len(minutes)):                              # Compare each pair of neighbors
            min_diff = min(min_diff, minutes[i] - minutes[i - 1])     # Difference between adjacent times

        circular = 1440 - (minutes[-1] - minutes[0])                  # Wrap-around: last → midnight → first
        min_diff = min(min_diff, circular)                             # Check if circular gap is smallest

        return min_diff                                               # Return the minimum difference


"""
WHY EACH PART:
    len > 1440:              Only 1440 possible minute values; duplicates guaranteed → diff = 0
    tp.split(":"):           Splits "13:45" into ["13", "45"]
    h * 60 + m:              Converts hours+minutes to total minutes (0-1439)
    minutes.sort():          After sorting, minimum diff must be between neighbors
    minutes[i] - minutes[i-1]: Difference between consecutive sorted times
    1440 - (last - first):   The "other way around" the clock (circular gap)
    min(min_diff, circular): The circular pair might be the smallest


HOW IT WORKS (Example: ["23:59", "00:00"]):

    Pigeonhole: 2 <= 1440 → continue

    Convert:
    ├── "23:59" → 23×60 + 59 = 1439
    └── "00:00" → 0×60 + 0   = 0

    Sort: [0, 1439]

    Adjacent pairs:
    └── 1439 - 0 = 1439

    Circular:
    └── 1440 - (1439 - 0) = 1

    min(1439, 1) = 1


HOW IT WORKS (Example: ["05:31", "22:08", "00:35"]):

    Convert:
    ├── "05:31" → 331
    ├── "22:08" → 1328
    └── "00:35" → 35

    Sort: [35, 331, 1328]

    Adjacent pairs:
    ├── 331 - 35   = 296
    └── 1328 - 331 = 997
    min_diff = 296

    Circular:
    └── 1440 - (1328 - 35) = 147

    min(296, 147) = 147


HOW IT WORKS (Example: ["00:00", "23:59", "00:00"]):

    Pigeonhole: 3 <= 1440 → continue

    Convert: [0, 1439, 0]

    Sort: [0, 0, 1439]

    Adjacent pairs:
    ├── 0 - 0 = 0         ← FOUND! Already 0
    └── (1439 - 0 = 1439)

    min_diff = 0  (duplicate times)


WHY SORTING GUARANTEES MINIMUM IS BETWEEN NEIGHBORS:
    Proof by contradiction:

    Suppose the minimum difference is between A and C,
    where A < B < C in the sorted order.

    Then: C - A = (C - B) + (B - A)
    
    Both (C - B) and (B - A) are positive.
    So: C - B < C - A  AND  B - A < C - A

    At least one neighbor pair is SMALLER than A,C pair.
    Contradiction! ✓

    Visual:
    ──A────B────────C──────
      ├──┤ ← smaller
      ├────────────┤ ← larger (skip B, always worse)


WHY THE CIRCULAR CASE IS ONLY LAST-TO-FIRST:
    After sorting: [t₀, t₁, t₂, ..., tₙ₋₁]

    All "forward" adjacent gaps are checked in the loop.
    The only unchecked gap is the "backward" one:
    
    ──t₀──t₁──t₂── ... ──tₙ₋₁──┐
    ↑                            │
    └────── circular gap ────────┘
    
    = 1440 - tₙ₋₁ + t₀ = 1440 - (tₙ₋₁ - t₀)

    We only need ONE circular comparison, always between
    the smallest and largest times.


WHY PIGEONHOLE PRINCIPLE WORKS:
    A day has exactly 1440 distinct minute values (00:00 to 23:59).

    If we have MORE than 1440 time points:
        By Pigeonhole Principle, at least two must be identical.
        Identical times → difference = 0 (minimum possible).

    This lets us return 0 immediately without any processing!

    ┌────────────────────────────────────┐
    │  1441 pigeons (times)              │
    │  1440 holes   (possible minutes)   │
    │  → At least 2 pigeons share a hole │
    │  → difference = 0                  │
    └────────────────────────────────────┘


HANDLING SPECIAL CASES:
    Duplicate times:       Adjacent after sort → diff = 0 ✓
    All same time:         diff = 0 ✓
    Two times only:        One adjacent + one circular comparison ✓
    Midnight wrap:         Circular formula handles it ✓
    Exactly "00:00":       Converts to 0 minutes ✓
    Exactly "23:59":       Converts to 1439 minutes ✓


KEY TECHNIQUE:
    Time to minutes:       Simplifies comparison to plain integers
    Sorting:               Guarantees minimum is between neighbors
    Circular comparison:   1440 - (last - first) handles wrap-around
    Pigeonhole principle:  Early exit for large inputs


EDGE CASES:
    ["00:00", "00:00"]:    0 (identical) ✓
    ["23:59", "00:00"]:    1 (circular) ✓
    ["00:00", "12:00"]:    720 (exactly half day) ✓
    ["00:00", "23:59", "00:00"]: 0 (duplicate) ✓
    1441+ time points:     0 (pigeonhole) ✓
    Two points max apart:  min(720, 720) = 720 ✓


TIME COMPLEXITY: O(n log n)
    Converting strings: O(n)
    Sorting: O(n log n) ← dominates
    Comparing neighbors: O(n)
    Overall: O(n log n)

SPACE COMPLEXITY: O(n)
    Array of converted minutes
    (Could be O(1) with bucket sort using 1440-size array,
     but sorting is cleaner for this constraint size)


CONCEPTS USED:
    Time conversion (HH:MM → total minutes)
    Sorting for minimum adjacent difference
    Circular/modular arithmetic (clock wrap-around)
    Pigeonhole principle (duplicate detection)
    Greedy approach (adjacent pairs in sorted order)
"""

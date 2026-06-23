# 1185. Day of the Week
# Difficulty: Easy
# https://leetcode.com/problems/day-of-the-week/

"""
PROBLEM:
Given a date consisting of `day`, `month`, and `year`, return the corresponding day of the week as a string.
The output must be one of: "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday".

EXAMPLES:
Input: day = 31, month = 8, year = 2019
Output: "Saturday"

Input: day = 15, month = 8, year = 1993
Output: "Sunday"

CONSTRAINTS:
- The given dates are valid dates between the years 1971 and 2100.

ALGORITHMIC INTUITION (THE "TRICK"):
While Python's `datetime` module can solve this in one line, algorithm interviews test your 
ability to logically simulate time. 
Since the problem guarantees years >= 1971, we can use an "Epoch" (Anchor Date) strategy.
We know for a fact that January 1st, 1971 was a Friday. 
If we count the EXACT number of days that have passed since Jan 1, 1971 until the target date, 
we can simply use Modulo 7 (`total_days % 7`) to find the exact day of the week.

The calculation has 3 parts:
1. Days from full passed years (1971 to year - 1), accounting for leap years.
2. Days from full passed months in the target year, accounting for leap years.
3. Days passed in the target month (day - 1).
"""

# STEP 1: Define arrays for standard days in a month and names of the days.
#         Notice the days array starts with "Friday" because Jan 1, 1971 was a Friday.
# STEP 2: Write a helper function for the Gregorian Leap Year rule.
# STEP 3: Accumulate days for all years strictly between 1971 and the target year.
# STEP 4: Accumulate days for all months strictly before the target month.
# STEP 5: Add an extra day if the current year is a leap year and we are past February.
# STEP 6: Accumulate the days of the current month (day - 1, since Jan 1st is day 0 of our epoch).
# STEP 7: Modulo 7 the total days and return the corresponding string.

class Solution:
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        
        # Step 1: Base data
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Since 1971-01-01 was a Friday, 0 shift means Friday.
        days_of_week = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        
        # Step 2: Leap year checker
        def is_leap(y: int) -> bool:
            return (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0)
            
        total_days = 0
        
        # Step 3: Add days for all strictly preceding years
        for y in range(1971, year):
            if is_leap(y):
                total_days += 366
            else:
                total_days += 365
                
        # Step 4: Add days for all strictly preceding months in the current year
        for m in range(month - 1):
            total_days += days_in_month[m]
            
        # Step 5: Handle leap year extra day for the current year
        if month > 2 and is_leap(year):
            total_days += 1
            
        # Step 6: Add the days of the target month
        # We subtract 1 because Jan 1st 1971 is our baseline (0 days passed)
        total_days += (day - 1)
        
        # Step 7: Map the sum to the correct day of the week
        return days_of_week[total_days % 7]

"""
WHY EACH PART:
- Starting the week array with "Friday": This aligns our modulo math perfectly. If 0 days have passed (Jan 1, 1971), 0 % 7 = 0 -> "Friday". If 1 day has passed (Jan 2, 1971), 1 % 7 = 1 -> "Saturday".
- day - 1: If the date is Jan 5, only 4 days have *passed* since Jan 1. Offset logic is crucial.

HOW IT WORKS (Example: day = 15, month = 8, year = 1993):
Anchor: 1971-01-01 (Friday)

1. Years Passed (1971 to 1992):
├── 22 years total. 5 were leap years, 17 were regular.
└── total_days += (5 * 366) + (17 * 365) = 8035

2. Months Passed (Jan to Jul 1993):
├── 1993 is NOT a leap year.
├── days = 31+28+31+30+31+30+31 = 212
└── total_days = 8035 + 212 = 8247

3. Days in Current Month:
├── day - 1 = 15 - 1 = 14
└── total_days = 8247 + 14 = 8261

4. Result Calculation:
├── 8261 % 7 = 2
└── days_of_week[2] = "Sunday" ✓

TIME COMPLEXITY: O(Y) - Where Y is the difference between the given year and 1971. In the worst case (year 2100), the loop runs ~130 times. This is effectively O(1) constant time.
SPACE COMPLEXITY: O(1) - Only small constant size arrays are used.

CONCEPTS USED:
- Date Simulation / Epoch Mathematics
- Modulo Arithmetic
- Prefix Summing
"""

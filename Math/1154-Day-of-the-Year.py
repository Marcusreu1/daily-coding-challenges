# 1154. Day of the Year
# Difficulty: Easy
# https://leetcode.com/problems/day-of-the-year/

"""
PROBLEM:
Given a string `date` representing a Gregorian calendar date formatted as YYYY-MM-DD, 
return the day number of the year.

EXAMPLES:
Input: date = "2019-01-09"
Output: 9
Explanation: Given date is the 9th day of the year in 2019.

Input: date = "2019-02-10"
Output: 41
Explanation: 31 days in January + 10 days in February = 41.

CONSTRAINTS:
- date.length == 10
- date[4] == date[7] == '-', and all other date[i]'s are digits
- date represents a calendar date between Jan 1st, 1900 and Dec 31st, 2019.

ALGORITHMIC INTUITION (THE "TRICK"):
The naive approach in Python would be to just use the `datetime` module. However, in an 
algorithm interview, the goal is to test your ability to implement the logic yourself.

The problem boils down to a Prefix Sum array calculation combined with the Leap Year rules.
1. Create a fixed array representing the days in each of the 12 months.
2. Parse the year, month, and day from the string.
3. Calculate the sum of the days from all the PREVIOUS months.
4. Add the current day.
5. If the year is a leap year AND the current month is strictly after February (> 2), add 1 extra day.

The Leap Year Algorithm:
A year is a leap year if it is divisible by 400 OR (divisible by 4 AND NOT divisible by 100).
"""

# STEP 1: Parse the string to extract year, month, and day as integers.
# STEP 2: Define a static array with the number of days in each month for a standard year.
# STEP 3: Implement the leap year mathematical check.
# STEP 4: Sum the days of all months strictly before the given month.
# STEP 5: Add the current day.
# STEP 6: Add 1 if it's a leap year and we are past February. Return the total.

class Solution:
    def dayOfYear(self, date: str) -> int:
        
        # Step 1: Parse the date
        # date format is "YYYY-MM-DD"
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        
        # Step 2: Array of days per month (Standard non-leap year)
        # Index corresponds to month - 1 (e.g., January is index 0)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Step 3: Calculate the prefix sum of previous months
        # If month is 3 (March), we sum indices 0 and 1 (Jan and Feb)
        total_days = sum(days_in_month[:month - 1])
        
        # Step 4: Add the days of the current month
        total_days += day
        
        # Step 5: Handle the Leap Year exception
        def is_leap_year(y: int) -> bool:
            # A year is leap if divisible by 400 OR (divisible by 4 and NOT by 100)
            return (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0)
            
        # We only add the extra leap day if we are PAST February (month > 2)
        if month > 2 and is_leap_year(year):
            total_days += 1
            
        return total_days

"""
WHY EACH PART:
- int(date[0:4]): String slicing is O(1) and the fastest way to extract fixed-format data without using the split() function array overhead.
- sum(days_in_month[:month - 1]): This is a mini prefix-sum. It dynamically calculates the base days before the current month.
- month > 2: A crucial condition! If the date is Feb 15th of a leap year, the extra day (Feb 29th) hasn't happened yet, so we don't count it.

HOW IT WORKS (Example: "2016-03-01"):
Initial: year = 2016, month = 3, day = 1

Prefix Sum Calculation:
├── We need months before March (indices 0 and 1)
├── days_in_month[:2] = [31, 28]
└── total_days = 31 + 28 = 59

Add Current Day:
└── total_days = 59 + 1 = 60

Leap Year Check:
├── is_leap_year(2016)? (2016 % 4 == 0) and (2016 % 100 != 0) -> True!
├── Is month > 2? (3 > 2) -> True!
└── Add 1. total_days = 60 + 1 = 61.

Return 61. ✓

TIME COMPLEXITY: O(1) - The operations are strictly bounded. The string parsing is a fixed 10 characters, the array is fixed at 12 elements. Constant time.
SPACE COMPLEXITY: O(1) - The array `days_in_month` is always exactly 12 integers long. No dynamic scaling occurs.

CONCEPTS USED:
- Prefix Sums
- String Parsing
- Mathematical Rule Implementation (Gregorian Calendar)
"""

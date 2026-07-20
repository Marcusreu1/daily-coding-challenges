# 1360. Number of Days Between Two Dates
# Difficulty: Easy
# https://leetcode.com/problems/number-of-days-between-two-dates/

"""
PROBLEM:
Write a program to count the number of days between two dates.
The two dates are given as strings, their format is YYYY-MM-DD.

EXAMPLES:
Input: date1 = "2019-06-29", date2 = "2019-06-30"
Output: 1
(Explanation: The dates are one day apart.)

Input: date1 = "2020-01-15", date2 = "2019-12-31"
Output: 15
(Explanation: 2020 is a leap year, but crossing the boundary from December 31st to Jan 15th represents exactly 15 days of absolute distance.)

CONSTRAINTS:
- The given dates are valid dates between the years 1971 and 2100.

ALGORITHM LOGIC (Abstraction via Standard Libraries):
1. Manual calendar arithmetic (leap years, variable month lengths) is highly error-prone and usually an anti-pattern in production environments.
2. We utilize Python's built-in `datetime.date` module to handle the parsing and arithmetic.
3. We parse the string by splitting it at the hyphens ('-') and casting the components (Year, Month, Day) to integers.
4. Instantiating two `date` objects allows us to subtract them using standard operators.
5. The subtraction of two `date` objects in Python yields a `timedelta` object.
6. Taking the absolute value (`abs()`) ensures the distance is always positive, regardless of chronological input order.
7. We extract the integer value from the `timedelta` via its `.days` attribute and return it.

VISUALIZATION:
date1 = "2020-01-15", date2 = "2019-12-31"

Step 1 (Parse date1):
Split "2020-01-15" -> ["2020", "01", "15"]
Cast to ints -> y=2020, m=1, d=15
Create object -> date(2020, 1, 15)

Step 2 (Parse date2):
Split "2019-12-31" -> ["2019", "12", "31"]
Cast to ints -> y=2019, m=12, d=31
Create object -> date(2019, 12, 31)

Step 3 (Arithmetic & Absolute Value):
date(2020, 1, 15) - date(2019, 12, 31) = timedelta(days=15)
abs(timedelta(days=15)) = timedelta(days=15)

Step 4 (Extraction):
timedelta(days=15).days = 15 ✓
"""

from datetime import date

# STEP 1: Import the `date` object from Python's standard `datetime` module
# STEP 2: Create a helper method to handle the string-to-date conversion cleanly
# STEP 3: Use `split` and `map` to extract year, month, and day integers
# STEP 4: Subtract the two generated date objects and apply `abs()` for a positive distance
# STEP 5: Return the `.days` property from the resulting timedelta object

class Solution:
    def daysBetweenDates(self, date1: str, date2: str) -> int:
        
        def parse_date(d_str: str) -> date:
            # Split the string by '-' and map the pieces into integer variables
            y, m, d = map(int, d_str.split('-'))
            return date(y, m, d)
        
        # Subtracting dates produces a timedelta object; abs() ensures it is positive
        time_delta = abs(parse_date(date1) - parse_date(date2))
        
        # Extract the exact integer of days from the timedelta object
        return time_delta.days

"""
WHY EACH PART:
- from datetime import date: Keeps the code memory-efficient by only bringing in the specific object we need, rather than the entire datetime suite.
- map(int, d_str.split('-')): This functional programming approach is significantly faster and more readable than using string slicing (e.g., d_str[0:4]) or regex to extract the numbers.
- abs(): Prevents negative results. date1 is not guaranteed to be chronologically after date2.
- time_delta.days: The subtraction resolves into a `datetime.timedelta` object under the hood. To satisfy the `-> int` return type hint, we must extract the integer property.

HOW IT WORKS (Example: "2019-06-29" and "2019-06-30"):
parse_date("2019-06-29") -> date(2019, 6, 29)
parse_date("2019-06-30") -> date(2019, 6, 30)
date(2019, 6, 29) - date(2019, 6, 30) -> timedelta(days=-1)
abs(timedelta(days=-1)) -> timedelta(days=1)
Returns 1. ✓

KEY TECHNIQUE:
- Native Standard Libraries (Avoiding reinvention of the wheel).
- Abstraction of complex domain logic (Calendar Math).
- String Manipulation and Type Mapping.

EDGE CASES:
- Leap years crossing (e.g., Feb 28 to Mar 1 on a leap year): Handled flawlessly by the C-backend of the datetime module. ✓
- Identical dates (e.g., "2000-01-01" to "2000-01-01"): timedelta(days=0). Returns 0. ✓

TIME COMPLEXITY: O(1) - The length of the strings is strictly fixed to 10 characters ("YYYY-MM-DD"). Splitting, mapping, and subtracting takes a constant amount of time regardless of how far apart the dates are.
SPACE COMPLEXITY: O(1) - We allocate a negligible, fixed amount of memory for the `date` objects.
"""

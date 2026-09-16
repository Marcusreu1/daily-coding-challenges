# 1904. The Number of Full Rounds You Have Played
# Difficulty: Medium
# https://leetcode.com/problems/the-number-of-full-rounds-you-have-played/

"""
PROBLEM:
You are participating in an online chess tournament. Here is how the tournament works:
- Matches start strictly at the beginning of each 15-minute interval: :00, :15, :30, and :45.
- A match lasts exactly 15 minutes.
- You can only play a full match if you are logged in from its start to its end.
You are given two strings loginTime and logoutTime in "HH:MM" format. 
Calculate the number of full matches you played. 
If logoutTime is earlier than loginTime, it means you played overnight (into the next day).

EXAMPLES:
Input: loginTime = "09:31", logoutTime = "10:14" → Output: 1
Explanation: 
You logged in at 09:31. The next match starts at 09:45.
You logged out at 10:14. You didn't finish the 10:00 match.
The only full match you played is from 09:45 to 10:00. (1 round).

Input: loginTime = "21:30", logoutTime = "03:00" → Output: 22
Explanation: 
You played overnight. 21:30 to 00:00 is 10 rounds. 00:00 to 03:00 is 12 rounds. 10 + 12 = 22 rounds.

CONSTRAINTS:
- loginTime and logoutTime are in the format "HH:MM".
- 00 <= HH <= 23, 00 <= MM <= 59.

MATH RULES (TIME NORMALIZATION & INTERVAL ALIGNMENT):
Working with hours and minutes separately is complicated. We convert all times into absolute "minutes from 00:00".
Formula: Total Minutes = (Hours * 60) + Minutes.
If loginTime > logoutTime, we crossed midnight. We handle this by adding a full day (24 hours * 60 minutes = 1440 minutes) to the logoutTime.

To find full 15-minute rounds:
- The player can only start a round on the NEXT multiple of 15. This is a mathematical "Ceiling". 
  We calculate the start round index using: (login_minutes + 14) // 15.
- The player can only finish a round on the PREVIOUS multiple of 15. This is a mathematical "Floor".
  We calculate the end round index using: logout_minutes // 15.
The total number of full rounds is simply: end_round - start_round.

VISUALIZATION (loginTime = "09:31", logoutTime = "10:14"):
Login: 9 * 60 + 31 = 571 minutes.
Logout: 10 * 60 + 14 = 614 minutes.

Start interval index: (571 + 14) // 15 = 585 // 15 = 39. (This represents the 09:45 block).
End interval index: 614 // 15 = 40. (This represents the 10:00 block).

Total rounds: 40 - 39 = 1.
Result: 1 ✓
"""

# STEP 1: Parse the string to extract hours and minutes, converting both times to absolute total minutes.
# STEP 2: Check for overnight sessions. If login > logout, add 1440 minutes to the logout time.
# STEP 3: Snap the login time FORWARD to the nearest 15-minute interval (Ceiling).
# STEP 4: Snap the logout time BACKWARD to the nearest 15-minute interval (Floor).
# STEP 5: Subtract start from end to get total rounds. Use max(0, result) to handle edge cases where start > end.

class Solution:
    def numberOfRounds(self, loginTime: str, logoutTime: str) -> int:
        
        # Convert HH:MM strings into total absolute minutes
        login_minutes = int(loginTime[:2]) * 60 + int(loginTime[3:])
        logout_minutes = int(logoutTime[:2]) * 60 + int(logoutTime[3:])
        
        # Handle the overnight boundary (crossing midnight)
        if login_minutes > logout_minutes:
            logout_minutes += 1440 # 24 hours * 60 minutes
            
        # Mathematically find the nearest starting round index (Ceil division)
        start_round = (login_minutes + 14) // 15
        
        # Mathematically find the nearest ending round index (Floor division)
        end_round = logout_minutes // 15
        
        # Calculate valid rounds, defaulting to 0 if the math yields a negative number
        return max(0, end_round - start_round)

"""
WHY EACH PART:
- loginTime[:2] / loginTime[3:]: Fast string slicing. Characters 0 and 1 are hours, character 2 is the colon, characters 3 and 4 are minutes.
- logout_minutes += 1440: Flattens the circular 24-hour clock into a linear mathematical timeline, making subtraction trivial.
- (login_minutes + 14) // 15: An efficient integer-math alternative to using math.ceil(login_minutes / 15.0).
- max(0, ...): Protects against scenarios where a user logs in and out quickly within the same 15-minute window (e.g., login 10:11, logout 10:12 -> start=41, end=40 -> 40 - 41 = -1).

KEY TECHNIQUE:
- Time Normalization: Converting composite units (hours, minutes) into a single scalar unit (total minutes).
- Grid Snapping (Ceil/Floor): Shifting start and end points to align with strict periodic boundaries mathematically rather than using while-loops.

EDGE CASES:
- Exact boundary times: login "10:00" -> (600 + 14)//15 = 40. Start index is exactly aligned. Handled flawlessly.
- Short session inside one block: "10:11" to "10:12" -> Returns max(0, -1) = 0.

TIME COMPLEXITY: O(1) - Converting strings and performing arithmetic operations takes constant time regardless of the times inputted.
SPACE COMPLEXITY: O(1) - The algorithm uses only a few integer variables.

CONCEPTS USED:
- Time & Date parsing
- Modular Arithmetic / Integer Division
- Boundary Alignment (Ceil/Floor)
"""

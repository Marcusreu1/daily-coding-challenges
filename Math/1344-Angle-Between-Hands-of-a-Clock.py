# 1344. Angle Between Hands of a Clock
# Difficulty: Medium
# https://leetcode.com/problems/angle-between-hands-of-a-clock/

"""
PROBLEM:
Given two numbers, hour and minutes, return the smaller angle (in degrees) formed 
between the hour and the minute hand.
Answers within 10^-5 of the actual value will be accepted as correct.

EXAMPLES:
Input: hour = 12, minutes = 30
Output: 165
(Explanation: 
Minute hand is at 30 minutes, pointing strictly at 6 (30 * 6° = 180°).
Hour hand has moved past 12 proportionally. At 30 minutes, it is exactly halfway 
between 12 and 1 (0° + 30 * 0.5° = 15°).
Difference = |15° - 180°| = 165°. This is smaller than 195°, so we return 165.)

Input: hour = 3, minutes = 30
Output: 75
(Explanation: 
Minute hand: 30 * 6° = 180°.
Hour hand: (3 * 30°) + (30 * 0.5°) = 90° + 15° = 105°.
Difference = |105° - 180°| = 75°.)

Input: hour = 3, minutes = 15
Output: 7.5

CONSTRAINTS:
- 1 <= hour <= 12
- 0 <= minutes <= 59

ALGORITHM LOGIC (Proportional Geometry):
1. Think of the clock as a 360° circle, with the 12 o'clock mark at 0°.
2. The minute hand moves 360° in 60 minutes. Therefore, it moves 6° per minute.
3. The hour hand moves 360° in 12 hours. Therefore, it moves 30° per hour.
4. The critical part: The hour hand also moves fractionally based on the minutes. 
   It moves 30° every 60 minutes, which equals 0.5° per minute.
5. The absolute difference between the two positions gives the angle.
6. A clock divides space into two angles that sum to 360°. We return min(angle, 360 - angle).

VISUALIZATION (hour = 3, minutes = 15):
Base origins at 12:00 = 0°

Minute hand position:
15 mins * 6° = 90°

Hour hand position:
Base 3 = 3 * 30° = 90°
Drift from minutes = 15 mins * 0.5° = 7.5°
Total hour position = 97.5°

Difference:
|97.5° - 90°| = 7.5°

Smaller angle check:
min(7.5°, 360° - 7.5°) = min(7.5°, 352.5°) = 7.5° ✓
"""

# STEP 1: Calculate the position of the minute hand in degrees
# STEP 2: Normalize the hour (12 becomes 0) using modulo 12
# STEP 3: Calculate the base position of the hour hand plus its proportional drift from minutes
# STEP 4: Find the absolute difference between both angles
# STEP 5: Return the minimum between the difference and its complement (360 - difference)

class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        
        minute_angle = minutes * 6                                   # 6 degrees per minute
        
        hour_angle = (hour % 12) * 30 + (minutes * 0.5)              # Base hour position + minute drift
        
        diff = abs(hour_angle - minute_angle)                        # Absolute difference between hands
        
        return min(diff, 360 - diff)                                 # Return the smaller of the two angles

"""
WHY EACH PART:
- minutes * 6: Simple linear rate. (360 degrees / 60 minutes).
- hour % 12: Normalizes 12 to 0. While mathematically (12 * 30) = 360 is the same point on a circle as 0, treating it as 0 keeps the difference calculation clean without needing a modulo 360 wrap-around later.
- minutes * 0.5: Simulates the mechanical gear connection. The hour hand doesn't snap to the next number; it drifts slowly.
- min(diff, 360 - diff): Ensures we always report the acute or obtuse internal angle (<= 180°), ignoring the external reflex angle (> 180°).

HOW IT WORKS (Example: hour = 12, minutes = 0):
minute_angle = 0 * 6 = 0
hour_angle = (0) * 30 + (0 * 0.5) = 0
diff = |0 - 0| = 0
min(0, 360 - 0) = 0. ✓

KEY TECHNIQUE:
- Mathematical Modeling: Translating a physical continuous system into discrete arithmetic formulas relative to a fixed origin point (0°).

EDGE CASES:
- Overlapping hands (e.g., 12:00): Both angles calculate to 0. Difference is 0. ✓
- Crossing hands (e.g., 12:30): The minute hand is ahead, handled flawlessly by the `abs()` function. ✓
- Hours at 12: Modulo ensures we don't start at a base of 360° avoiding wrap-around complexity. ✓

TIME COMPLEXITY: O(1) - The algorithm performs a fixed number of basic arithmetic operations regardless of the input values. It runs in constant time.
SPACE COMPLEXITY: O(1) - We only store three floating-point variables (`minute_angle`, `hour_angle`, `diff`). No extra memory scaling is used.

CONCEPTS USED:
- Proportional Geometry
- Modulo Arithmetic
- Absolute Values
"""

# 2469. Convert the Temperature
# Difficulty: Easy
# https://leetcode.com/problems/convert-the-temperature/

"""
PROBLEM:
You are given a non-negative floating point number rounded to two decimal places celsius, that denotes the temperature in Celsius.
You should convert Celsius into Kelvin and Fahrenheit and return it as an array ans = [kelvin, fahrenheit].
Answers within 10^-5 of the actual answer will be accepted.

Conversion formulas:
- Kelvin = Celsius + 273.15
- Fahrenheit = Celsius * 1.80 + 32.00

EXAMPLES:
Input: celsius = 36.50 → Output: [309.65000, 97.70000]
Explanation: 
- Kelvin = 36.50 + 273.15 = 309.65
- Fahrenheit = 36.50 * 1.80 + 32.00 = 97.70

CONSTRAINTS:
- 0 <= celsius <= 1000

MATH RULES (LINEAR SCALING & TRANSLATION):
- Kelvin conversion applies an affine translation (adding a fixed constant offset).
- Fahrenheit conversion applies a linear scaling factor (multiplication by 1.80) followed by a constant offset (adding 32.00).
Both operations execute in hardware-level floating-point units in O(1) time.
"""

from typing import List

# STEP 1: Compute Kelvin by adding 273.15 to the celsius value.
# STEP 2: Compute Fahrenheit by multiplying celsius by 1.80 and adding 32.00.
# STEP 3: Return both values packaged inside a 2-element list.

class Solution:
    def convertTemperature(self, celsius: float) -> List[float]:
        
        # Direct linear transformation mapping Celsius to Kelvin and Fahrenheit
        return [celsius + 273.15, celsius * 1.80 + 32.00]

"""
WHY EACH PART:
- celsius + 273.15: Direct execution of the absolute thermodynamic temperature offset.
- celsius * 1.80 + 32.00: Strict adherence to the Fahrenheit scale conversion rule (respecting standard algebraic operator precedence).

KEY TECHNIQUE:
- Stateless Linear Evaluation: Performing deterministic scalar calculations without internal state dependencies or iterations.

EDGE CASES:
- celsius = 0.0: Returns [273.15, 32.00]. Correct freezing point behavior.
- Upper boundary (celsius = 1000.0): Computes without floating-point overflow or precision loss.

TIME COMPLEXITY: O(1) - Evaluates two arithmetic expressions in constant time.
SPACE COMPLEXITY: O(1) - Allocates a static list of 2 floats.
"""

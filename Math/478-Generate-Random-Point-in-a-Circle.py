"""
478. Generate Random Point in a Circle
Difficulty: Medium
https://leetcode.com/problems/generate-random-point-in-a-circle/

PROBLEM:
Given the radius and the position of the center of a circle,
implement the function randPoint which generates a uniform random
point inside the circle (including on the boundary).

EXAMPLES:
Input: radius=1, x_center=0, y_center=0
    randPoint() → [-0.02493, -0.38077]
    randPoint() → [0.82314, 0.38945]
    randPoint() → [0.36572, 0.17248]

CONSTRAINTS:
    0 < radius <= 10^8
    -10^7 <= x_center, y_center <= 10^7
    At most 3 × 10^4 calls to randPoint

KEY INSIGHT:
Naive r = random() × radius concentrates points at center because
outer rings have MORE AREA but receive SAME proportion of r values.

Fix: r = √(random()) × radius. The square root compensates for the
quadratic growth of area with radius, giving uniform distribution.

CHALLENGES:
    Naive random radius gives non-uniform distribution
    Understanding why area grows with r² (not r)
    Correctly converting polar to cartesian coordinates

WHY √(random()):
    Area within radius r: A(r) = πr²
    For uniformity: P(point within r) = r²/R²
    If u ~ Uniform[0,1], then r = R√u gives P(r ≤ r₀) = r₀²/R² ✓

SOLUTION:
    1. Random angle θ in [0, 2π)
    2. Random radius r = √(random()) × radius
    3. Convert polar to cartesian: (r×cos(θ), r×sin(θ))
    4. Add center offset
"""

# STEP 1: Store circle parameters in __init__
# STEP 2: Generate random angle and corrected radius in randPoint
# STEP 3: Convert to cartesian and offset by center

import random
import math

class Solution:

    def __init__(self, radius: float, x_center: float, y_center: float):
        self.radius = radius                                             # Circle radius
        self.x = x_center                                               # Center x coordinate
        self.y = y_center                                                # Center y coordinate

    def randPoint(self) -> List[float]:
        theta = random.uniform(0, 2 * math.pi)                          # Random angle [0, 2π)
        r = math.sqrt(random.random()) * self.radius                     # √(uniform) × R for area-uniform radius

        return [self.x + r * math.cos(theta),                           # Polar → cartesian + center offset (x)
                self.y + r * math.sin(theta)]                            # Polar → cartesian + center offset (y)

"""
WHY EACH PART:

    self.radius, self.x, self.y: Store circle params for repeated use
    random.uniform(0, 2*math.pi): Uniform angle covers full rotation
    random.random(): Uniform in [0, 1)
    math.sqrt(...): Square root correction for area-uniform distribution
    * self.radius: Scale to actual circle size
    r * math.cos(theta): Polar to cartesian x component
    r * math.sin(theta): Polar to cartesian y component
    self.x + ..., self.y + ...: Offset from origin to actual center

HOW IT WORKS (Example: radius=2, center=(3,5)):

    Call randPoint():
    ├── theta = uniform(0, 6.283) → say 1.047 (≈60°)
    ├── u = random() → say 0.49
    ├── r = √0.49 × 2 = 0.7 × 2 = 1.4
    ├── x = 3 + 1.4 × cos(1.047) = 3 + 1.4 × 0.5 = 3.7
    ├── y = 5 + 1.4 × sin(1.047) = 5 + 1.4 × 0.866 = 6.21
    └── return [3.7, 6.21]

    Verify: distance to center = √((3.7-3)² + (6.21-5)²)
            = √(0.49 + 1.46) = √1.95 = 1.4 ≤ 2 ✓

WHY √(random()) GIVES UNIFORM DISTRIBUTION:

    Without √ (WRONG):
    ├── r = random() × R
    ├── P(r ≤ R/2) = 0.5         (50% of points in inner half)
    ├── Area of inner half = π(R/2)² = πR²/4 = 25% of total area
    └── 50% of points in 25% of area → concentrated at center ✗

    With √ (CORRECT):
    ├── r = √(random()) × R
    ├── P(r ≤ R/2) = P(√u × R ≤ R/2) = P(u ≤ 1/4) = 0.25
    ├── Area of inner half = 25% of total area
    └── 25% of points in 25% of area → uniform ✓

    General: P(r ≤ r₀) = P(√u ≤ r₀/R) = P(u ≤ r₀²/R²) = r₀²/R²
    This equals area(r₀)/area(R) = πr₀²/πR² → uniform by area ✓

MATHEMATICAL DERIVATION:

    Want: CDF of r to match area proportion
        F(r) = P(point within radius r) = πr² / πR² = r²/R²

    Inverse CDF method (to sample from this distribution):
        u = random()  [uniform 0 to 1]
        u = r²/R²     [set equal to CDF]
        r² = u × R²
        r = R × √u    ← our formula!

    This is the standard "inverse transform sampling" technique.

WHY NOT JUST RANDOM X AND Y IN A SQUARE:

    Rejection sampling approach:
        x = uniform(-R, R),  y = uniform(-R, R)
        if x² + y² ≤ R²: accept
        else: reject and retry

    Works! But:
    ├── P(accept) = πR²/(2R)² = π/4 ≈ 78.5%
    ├── Expected attempts = 4/π ≈ 1.27
    ├── ~21.5% of random numbers wasted
    └── Slightly less efficient than polar method

    Polar with √ method:
    ├── Always succeeds on first try
    ├── No wasted random numbers
    ├── Exactly 2 random numbers per point
    └── More elegant ✓

POLAR TO CARTESIAN CONVERSION:

    Given polar coordinates (r, θ):
        x = r × cos(θ)     ← horizontal component
        y = r × sin(θ)     ← vertical component

    This maps a point at distance r, angle θ from origin
    to its (x, y) cartesian coordinates.

    Adding center offset (cx, cy):
        final_x = cx + r × cos(θ)
        final_y = cy + r × sin(θ)

    This shifts the circle from origin to its actual position.

VISUAL: RING AREAS AND POINT DISTRIBUTION:

    Ring from r=0.0 to 0.2:  area = π(0.04) = 0.126
    Ring from r=0.2 to 0.4:  area = π(0.12) = 0.377    ← 3x more!
    Ring from r=0.4 to 0.6:  area = π(0.20) = 0.628    ← 5x more!
    Ring from r=0.6 to 0.8:  area = π(0.28) = 0.880    ← 7x more!
    Ring from r=0.8 to 1.0:  area = π(0.36) = 1.131    ← 9x more!

    √(random()) assigns proportionally MORE r-values to outer rings:
    ├── P(r in [0.0, 0.2]) = 0.04  (4% of points in 4% of area) ✓
    ├── P(r in [0.2, 0.4]) = 0.12  (12% in 12%) ✓
    ├── P(r in [0.4, 0.6]) = 0.20  (20% in 20%) ✓
    ├── P(r in [0.6, 0.8]) = 0.28  (28% in 28%) ✓
    └── P(r in [0.8, 1.0]) = 0.36  (36% in 36%) ✓

EDGE CASES:

    Center at origin (0,0): Offset is 0, simplest case ✓
    Very small radius (0.001): Still generates valid points ✓
    Very large radius (10^8): Floating point precision sufficient ✓
    Negative center coordinates: Offset works naturally ✓
    Point on boundary: √1 × R = R → exactly on edge, valid ✓
    Point at center: √0 × R = 0 → exactly at center, valid ✓
    Many calls (3×10^4): Each O(1), total O(n) ✓

TIME COMPLEXITY: O(1) per call
    Two random numbers, one sqrt, one cos, one sin
    All constant time operations

SPACE COMPLEXITY: O(1)
    Only stores radius and center (3 values)
    Each call uses constant extra space

CONCEPTS USED:
    Polar coordinate system (r, θ)
    Inverse transform sampling (√ correction)
    Area-proportional probability distribution
    Polar to cartesian conversion
    Rejection sampling (alternative approach)
    Probability density vs cumulative distribution
"""

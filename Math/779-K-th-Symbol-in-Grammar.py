"""
779. K-th Symbol in Grammar
Difficulty: Medium
https://leetcode.com/problems/k-th-symbol-in-grammar/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

We start with row 1 containing a single symbol:

    Row 1: 0

To generate the next row, every symbol is replaced using the rules:

    0 → 01
    1 → 10

Given two integers n and k, return the kth symbol in row n.

Important:
    k is 1-indexed.

EXAMPLES:

    Input: n = 1, k = 1
    Output: 0

    Input: n = 2, k = 1
    Output: 0

    Input: n = 2, k = 2
    Output: 1

    Input: n = 4, k = 5
    Output: 1

ROWS:

    Row 1: 0
    Row 2: 0 1
    Row 3: 0 1 1 0
    Row 4: 0 1 1 0 1 0 0 1

CONSTRAINTS:

    1 <= n <= 30
    1 <= k <= 2^(n - 1)

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Each symbol in row n comes from exactly one parent symbol in row n-1.

The replacement rules are:

    Parent 0 → children 0 1
    Parent 1 → children 1 0

So:

    Left child  = same as parent
    Right child = opposite of parent

For a position k in row n:

    If k is odd:
        The kth symbol is a LEFT child.
        Therefore, it is equal to its parent.

    If k is even:
        The kth symbol is a RIGHT child.
        Therefore, it is the opposite of its parent.

The parent index in the previous row is:

    ceil(k / 2)

In integer arithmetic:

    parent_index = k // 2 + k % 2

or equivalently:

    parent_index = (k + 1) // 2

════════════════════════════════════════════════════════════════
MATHEMATICAL RECURRENCE:
════════════════════════════════════════════════════════════════

Let f(n, k) be the kth symbol in row n.

Base case:

    f(1, 1) = 0

For n > 1:

    parent = f(n - 1, ceil(k / 2))

Then:

    If k is odd:
        f(n, k) = parent

    If k is even:
        f(n, k) = 1 - parent

This works because every symbol has a unique parent in the row above.

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: If n == 1, return 0
STEP 2: Find the parent index in row n - 1
STEP 3: Recursively compute the parent value
STEP 4: If k is odd, return the parent value
STEP 5: If k is even, return the opposite of the parent value
"""


class Solution:
    def kthGrammar(self, n: int, k: int) -> int:

        # Base case:
        # The first row contains only one symbol: 0.
        if n == 1:
            return 0

        # Parent index in the previous row.
        #
        # Since each parent produces two children:
        #   parent 1 produces positions 1 and 2
        #   parent 2 produces positions 3 and 4
        #   parent 3 produces positions 5 and 6
        #
        # Therefore, the parent of position k is ceil(k / 2).
        #
        # k // 2 + k % 2 is an integer way to compute ceil(k / 2):
        #   if k is even: k // 2 + 0
        #   if k is odd:  k // 2 + 1
        parent_index = k // 2 + k % 2

        # Recursively find the value of the parent symbol.
        parent_value = self.kthGrammar(n - 1, parent_index)

        # Determine whether the current position is a left or right child.
        #
        # If k is odd:
        #   k % 2 == 1
        #   The current symbol is the LEFT child.
        #   Left child is the SAME as the parent.
        #
        # If k is even:
        #   k % 2 == 0
        #   The current symbol is the RIGHT child.
        #   Right child is the OPPOSITE of the parent.
        #
        # The expression int(parent_value == k % 2) encodes both cases:
        #
        # Case 1: k is odd
        #   k % 2 = 1
        #   return int(parent_value == 1)
        #   If parent is 1 → return 1
        #   If parent is 0 → return 0
        #   This returns parent_value.
        #
        # Case 2: k is even
        #   k % 2 = 0
        #   return int(parent_value == 0)
        #   If parent is 0 → return 1
        #   If parent is 1 → return 0
        #   This returns 1 - parent_value.
        return int(parent_value == k % 2)


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

if n == 1:
    return 0

    This is the base case.
    Row 1 is always:

        0

    So the only possible answer in row 1 is 0.

parent_index = k // 2 + k % 2

    Every symbol in row n comes from a parent in row n - 1.

    Each parent generates two children:

        Parent index 1 → child positions 1 and 2
        Parent index 2 → child positions 3 and 4
        Parent index 3 → child positions 5 and 6

    Therefore, the parent of position k is:

        ceil(k / 2)

    Examples:

        k = 1 → parent = 1
        k = 2 → parent = 1
        k = 3 → parent = 2
        k = 4 → parent = 2
        k = 5 → parent = 3
        k = 6 → parent = 3

    The formula:

        k // 2 + k % 2

    computes ceil(k / 2).

parent_value = self.kthGrammar(n - 1, parent_index)

    Once we know the parent index, we recursively compute the
    parent symbol from the previous row.

    This reduces the problem from:

        f(n, k)

    to:

        f(n - 1, parent_index)

return int(parent_value == k % 2)

    This compact expression handles both child cases.

    The grammar rules are:

        0 → 01
        1 → 10

    Meaning:

        Left child  = same as parent
        Right child = opposite of parent

    If k is odd:
        The current symbol is a left child.
        k % 2 = 1.

        return int(parent_value == 1)

        If parent_value = 1 → return 1
        If parent_value = 0 → return 0

        So this returns the parent value.

    If k is even:
        The current symbol is a right child.
        k % 2 = 0.

        return int(parent_value == 0)

        If parent_value = 0 → return 1
        If parent_value = 1 → return 0

        So this returns the opposite of the parent value.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 4, k = 5):
════════════════════════════════════════════════════════════════

Rows:

    Row 1: 0
    Row 2: 0 1
    Row 3: 0 1 1 0
    Row 4: 0 1 1 0 1 0 0 1
                    ↑
                   k=5

Recursive trace:

    kthGrammar(4, 5)

    k = 5 is odd
    parent_index = 5 // 2 + 5 % 2
                 = 2 + 1
                 = 3

    parent_value = kthGrammar(3, 3)

        kthGrammar(3, 3)

        k = 3 is odd
        parent_index = 3 // 2 + 3 % 2
                     = 1 + 1
                     = 2

        parent_value = kthGrammar(2, 2)

            kthGrammar(2, 2)

            k = 2 is even
            parent_index = 2 // 2 + 2 % 2
                         = 1 + 0
                         = 1

            parent_value = kthGrammar(1, 1)

                kthGrammar(1, 1)
                return 0

            parent_value = 0
            k % 2 = 0

            return int(parent_value == k % 2)
            return int(0 == 0)
            return 1

        parent_value = 1
        k % 2 = 1

        return int(parent_value == k % 2)
        return int(1 == 1)
        return 1

    parent_value = 1
    k % 2 = 1

    return int(parent_value == k % 2)
    return int(1 == 1)
    return 1

Answer: 1 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 4, k = 6):
════════════════════════════════════════════════════════════════

Rows:

    Row 4: 0 1 1 0 1 0 0 1
                      ↑
                     k=6

Recursive trace:

    kthGrammar(4, 6)

    k = 6 is even
    parent_index = 6 // 2 + 6 % 2
                 = 3 + 0
                 = 3

    parent_value = kthGrammar(3, 3)

        kthGrammar(3, 3)

        k = 3 is odd
        parent_index = 3 // 2 + 3 % 2
                     = 1 + 1
                     = 2

        parent_value = kthGrammar(2, 2)

            kthGrammar(2, 2)

            k = 2 is even
            parent_index = 2 // 2 + 2 % 2
                         = 1 + 0
                         = 1

            parent_value = kthGrammar(1, 1)
            parent_value = 0

            k % 2 = 0
            return int(0 == 0)
            return 1

        parent_value = 1

        k % 2 = 1
        return int(1 == 1)
        return 1

    parent_value = 1

    k % 2 = 0
    return int(1 == 0)
    return 0

Answer: 0 ✓

════════════════════════════════════════════════════════════════
PARENT-CHILD RELATIONSHIP:
════════════════════════════════════════════════════════════════

The grammar rules are:

    0 → 01
    1 → 10

This means every parent creates two children.

For parent = 0:

    left child  = 0
    right child = 1

For parent = 1:

    left child  = 1
    right child = 0

So:

    left child  = parent
    right child = 1 - parent

Now connect this to k:

    If k is odd:
        k is a left child.
        answer = parent

    If k is even:
        k is a right child.
        answer = 1 - parent

════════════════════════════════════════════════════════════════
WHY parent_index = ceil(k / 2):
════════════════════════════════════════════════════════════════

Each parent produces exactly two children:

    Parent 1:
        child positions 1 and 2

    Parent 2:
        child positions 3 and 4

    Parent 3:
        child positions 5 and 6

    Parent 4:
        child positions 7 and 8

So the mapping is:

    k = 1 → parent 1
    k = 2 → parent 1
    k = 3 → parent 2
    k = 4 → parent 2
    k = 5 → parent 3
    k = 6 → parent 3

This is exactly:

    parent_index = ceil(k / 2)

In Python integer arithmetic:

    ceil(k / 2) = k // 2 + k % 2

or:

    ceil(k / 2) = (k + 1) // 2

Both are valid.

════════════════════════════════════════════════════════════════
WHY return int(parent_value == k % 2) WORKS:
════════════════════════════════════════════════════════════════

This line is a compact mathematical encoding of the two cases.

Case 1: k is odd

    k % 2 = 1

    return int(parent_value == 1)

    If parent_value = 0:
        int(0 == 1) = 0

    If parent_value = 1:
        int(1 == 1) = 1

    This returns parent_value.

Case 2: k is even

    k % 2 = 0

    return int(parent_value == 0)

    If parent_value = 0:
        int(0 == 0) = 1

    If parent_value = 1:
        int(1 == 0) = 0

    This returns 1 - parent_value.

Therefore:

    int(parent_value == k % 2)

is equivalent to:

    if k is odd:
        return parent_value
    else:
        return 1 - parent_value

════════════════════════════════════════════════════════════════
MORE READABLE VERSION:
════════════════════════════════════════════════════════════════

The same logic can be written more explicitly:

    class Solution:
        def kthGrammar(self, n: int, k: int) -> int:
            if n == 1:
                return 0

            parent_index = (k + 1) // 2
            parent_value = self.kthGrammar(n - 1, parent_index)

            if k % 2 == 1:
                return parent_value
            else:
                return 1 - parent_value

This version is easier to understand.

The compact version:

    return int(parent_value == k % 2)

does the same thing in one line.

════════════════════════════════════════════════════════════════
WHY WE DO NOT BUILD THE ROW:
════════════════════════════════════════════════════════════════

Building the full row is too expensive.

Row lengths:

    Row 1 length = 1
    Row 2 length = 2
    Row 3 length = 4
    Row 4 length = 8
    ...
    Row n length = 2^(n - 1)

For n = 30:

    Row length = 2^29 = 536,870,912

That is far too large to generate.

The recursive mathematical solution avoids building the row.
It only follows one path from row n back to row 1.

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    n = 1, k = 1
        Base case.
        Return 0 ✓

    k = 1
        Always follows left-child links.
        Left child is always same as parent.
        Since root is 0, answer is 0 ✓

    n = 2, k = 2
        Parent is row 1, index 1 → 0
        k is even → right child → opposite of 0 → 1 ✓

    n = 4, k = 5
        Parent chain leads to value 1.
        Answer = 1 ✓

    n = 4, k = 6
        Parent value is 1.
        k is even → opposite → 0 ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

Each recursive call moves from row n to row n - 1.

    kthGrammar(n, k)
    kthGrammar(n - 1, parent)
    kthGrammar(n - 2, parent)
    ...
    kthGrammar(1, 1)

There are exactly n recursive levels.

Total time:

    O(n)

Since n <= 30, this is very fast.

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

The recursion stack has one frame per row.

Maximum recursion depth:

    n

Total auxiliary space:

    O(n)

Since n <= 30, this is safe.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Mathematical recurrence
    Recursive decomposition
    Parent-child relationship
    Binary tree interpretation
    Parity checking
    Integer ceiling division
    Symbol inversion
    Avoiding exponential construction
"""

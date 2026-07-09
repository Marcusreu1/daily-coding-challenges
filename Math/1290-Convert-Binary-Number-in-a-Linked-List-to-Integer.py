# 1290. Convert Binary Number in a Linked List to Integer
# Difficulty: Easy
# https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/

"""
PROBLEM:
Given head which is a reference node to a singly-linked list. The value of each node 
in the linked list is either 0 or 1. The linked list holds the binary representation of a number.
Return the decimal value of the number in the linked list.
The most significant bit is at the head of the linked list.

EXAMPLES:
Input: head = [1,0,1]
Output: 5
(Explanation: The linked list represents the binary number 101. 
Binary 101 in decimal is: (1 * 2^2) + (0 * 2^1) + (1 * 2^0) = 4 + 0 + 1 = 5.)

Input: head = [0]
Output: 0
(Explanation: Binary 0 in decimal is 0.)

CONSTRAINTS:
- The Linked List is not empty.
- Number of nodes will not exceed 30.
- Each node's value is either 0 or 1.

ALGORITHM LOGIC (Bitwise/Mathematical Accumulation):
1. Unlike arrays, we cannot access linked lists by index. We must traverse it node by node.
2. Instead of storing the sequence as a string and parsing it at the end, we can compute 
   the decimal value on the fly.
3. In a positional numeral system (like base-2), appending a new digit to the right implies 
   shifting all previously read digits one position to the left.
4. Shifting left in base-2 is mathematically equivalent to multiplying the current value by 2.
5. Therefore, at each node, the new total is: (current_total * 2) + node_value.

VISUALIZATION (head = [1,0,1]):
Initial State:
decimal_value = 0

Iteration 1 (Node Value = 1):
decimal_value = (0 * 2) + 1 = 1
Move to next node.

Iteration 2 (Node Value = 0):
decimal_value = (1 * 2) + 0 = 2
Move to next node.

Iteration 3 (Node Value = 1):
decimal_value = (2 * 2) + 1 = 5
Move to next node.

Loop Ends (Next node is None).
Result = 5 ✓
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# STEP 1: Initialize the decimal_value accumulator to 0
# STEP 2: Loop while the current node (head) is not None
# STEP 3: Multiply the current decimal_value by 2 and add the node's value
# STEP 4: Move the pointer to the next node in the linked list
# STEP 5: Return the fully accumulated decimal_value

class Solution:
    def getDecimalValue(self, head) -> int:
        
        decimal_value = 0                                            # Accumulator for the final decimal result
        
        while head:                                                  # Traverse until the end of the list (None)
            
            decimal_value = decimal_value * 2 + head.val             # Shift previous bits left and add new bit
            
            head = head.next                                         # Move pointer to the next node
            
        return decimal_value                                         # Return the final integer

"""
WHY EACH PART:
- decimal_value = 0: We start with an additive identity that cleanly absorbs the first multiplication (0 * 2 = 0).
- while head: This is the standard idiom in Python for linked list traversal. It evaluates to True as long as the node object exists.
- decimal_value * 2 + head.val: This avoids the need for Python's built-in `int(string, 2)` function, bypassing string concatenations entirely.
- head = head.next: The only way to move forward in a singly linked list. If we forget this, we create an infinite loop.

HOW IT WORKS (Example: head = [1,1]):
decimal_value = 0
Node 1 (val=1): decimal_value = (0 * 2) + 1 = 1. head moves.
Node 2 (val=1): decimal_value = (1 * 2) + 1 = 3. head moves to None.
Returns 3. ✓

KEY TECHNIQUE:
- Linked List Traversal: Following `next` pointers.
- On-the-fly Base Conversion: Using the `total = total * base + current_val` formula.
- Bitwise Alternative: The math `decimal_value * 2 + head.val` can also be written using bitwise operators as `(decimal_value << 1) | head.val`, which is identical under the hood but conceptually identical.

EDGE CASES:
- Only one node containing 0: decimal_value = 0 * 2 + 0 = 0. Works perfectly. ✓
- Up to 30 nodes: Python handles arbitrarily large integers automatically, so a 30-bit number will not overflow. Works perfectly. ✓

TIME COMPLEXITY: O(N) - Where N is the number of nodes in the linked list. We visit each node exactly once.
SPACE COMPLEXITY: O(1) - We only use a single integer variable (`decimal_value`), regardless of the linked list's size. No extra memory is allocated.

CONCEPTS USED:
- Singly-Linked Lists
- Base-2 to Base-10 Arithmetic
- Iterative Traversal
"""

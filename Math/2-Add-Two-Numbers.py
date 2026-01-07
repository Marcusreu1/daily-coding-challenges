# 2. Add Two Numbers
# Difficulty: Medium
# https://leetcode.com/problems/add-two-numbers/

"""
PROBLEM:
Given two non-empty linked lists representing two non-negative integers.
Digits are stored in REVERSE order (units first). Each node contains a single digit.
Add the two numbers and return the sum as a linked list (also in reverse order).

DATA STRUCTURE:
- ListNode: val (0-9), next (pointer to next node or None)

EXAMPLES:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
Explanation: 9999999 + 9999 = 10009998

CONSTRAINTS:
- Number of nodes: [1, 100]
- Node.val: [0, 9]
- No leading zeros (except 0 itself)
"""

# STEP 1: Initialize dummy node to simplify head management
# STEP 2: Iterate while there are digits in either list OR carry exists
# STEP 3: Get values from both lists (0 if list exhausted)
# STEP 4: Calculate sum and extract digit and carry
# STEP 5: Create new node with the digit
# STEP 6: Advance pointers in original lists
# STEP 7: Return dummy.next (skip the dummy node)

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        dummy = ListNode(0)                                                      # Dummy node simplifies head handling
        current = dummy                                                          # Pointer to build result list
        carry = 0                                                                # Carry for addition (0 or 1)
        
        while l1 or l2 or carry:                                                 # Continue while there's work to do
            
            val1 = l1.val if l1 else 0                                           # Get digit from l1 (0 if exhausted)
            val2 = l2.val if l2 else 0                                           # Get digit from l2 (0 if exhausted)
            
            total = val1 + val2 + carry                                          # Sum digits plus carry
            carry = total // 10                                                  # New carry: 1 if total >= 10, else 0
            digit = total % 10                                                   # Current digit to store
            
            current.next = ListNode(digit)                                       # Create new node with digit
            current = current.next                                               # Move pointer forward
            
            l1 = l1.next if l1 else None                                         # Advance l1 if not exhausted
            l2 = l2.next if l2 else None                                         # Advance l2 if not exhausted
        
        return dummy.next                                                        # Return head (skip dummy)

"""
WHY EACH PART:
- dummy node: Avoids special case for creating head of result list
- carry variable: Handles overflow when sum >= 10
- while l1 or l2 or carry: Three conditions ensure we process all digits AND final carry
- val if l1 else 0: Handles lists of different lengths gracefully
- total // 10: Integer division gives carry (0 or 1)
- total % 10: Modulo gives the digit to store (0-9)
- l1.next if l1 else None: Safe advancement prevents NoneType errors

HOW IT WORKS (Example: [2,4,3] + [5,6,4]):
Step 1: 2 + 5 + 0 = 7  → digit=7, carry=0 → Result: [7]
Step 2: 4 + 6 + 0 = 10 → digit=0, carry=1 → Result: [7,0]
Step 3: 3 + 4 + 1 = 8  → digit=8, carry=0 → Result: [7,0,8]
Final: No more nodes, carry=0 → Return [7,0,8] ✓

KEY TECHNIQUE:
- Digit-by-digit addition: Mirrors manual addition process
- Reverse order advantage: Natural left-to-right traversal = units to higher places
- Dummy node pattern: Common linked list technique for cleaner code
- Carry propagation: carry = total // 10 handles all overflow cases

EDGE CASES:
- Both single digit [5] + [5] = [0,1] (5+5=10) ✓
- Single zeros [0] + [0] = [0] ✓
- Different lengths [9,9] + [1] = [0,0,1] (99+1=100) ✓
- Carry at end [9,9,9] + [1] = [0,0,0,1] ✓
- No carry needed [1,2,3] + [4,5,6] = [5,7,9] ✓
- Maximum digits (100 nodes each): Works within constraints ✓

CONCEPTS USED:
- Linked List traversal
- Dummy/sentinel node pattern
- Carry propagation in addition
- Integer division and modulo operations
- Multiple pointer technique
- Handling None/null safely
"""

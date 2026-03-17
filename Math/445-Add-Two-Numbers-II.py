"""
445. Add Two Numbers II
Difficulty: Medium
https://leetcode.com/problems/add-two-numbers-ii/

PROBLEM:
You are given two non-empty linked lists representing two non-negative
integers. The most significant digit comes first and each node contains
a single digit. Add the two numbers and return the sum as a linked list.

You may not modify the input lists.

EXAMPLES:
Input: l1 = [7,2,4,3], l2 = [5,6,4]  → Output: [7,8,0,7]
    7243 + 564 = 7807

Input: l1 = [2,4,3], l2 = [5,6,4]    → Output: [8,0,7]
    243 + 564 = 807

Input: l1 = [0], l2 = [0]            → Output: [0]

CONSTRAINTS:
    Number of nodes in each list: [1, 100]
    0 <= Node.val <= 9
    No leading zeros (except 0 itself)
    Must NOT modify the input lists

KEY INSIGHT:
Addition goes RIGHT to LEFT, but linked lists go LEFT to RIGHT.
Use STACKS to reverse the access order without modifying the lists.
Then build the result by PREPENDING nodes (right to left construction).

CHALLENGES:
    Digits in forward order but addition needs reverse order
    Lists can have different lengths
    Cannot modify input lists
    Carry propagation and final carry

SOLUTION:
    1. Push all digits onto stacks (reverses access order)
    2. Pop from both stacks, add with carry
    3. Prepend each digit to result list
    4. Handle remaining carry
"""

# STEP 1: Push digits of both lists onto stacks
# STEP 2: Pop and add digits with carry
# STEP 3: Prepend each result digit to build list right-to-left
# STEP 4: Handle final carry

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:

        stack1 = []                                                      # Stack for l1 digits
        stack2 = []                                                      # Stack for l2 digits

        while l1:                                                        # Push all l1 digits
            stack1.append(l1.val)
            l1 = l1.next

        while l2:                                                        # Push all l2 digits
            stack2.append(l2.val)
            l2 = l2.next

        carry = 0                                                        # Carry for addition
        head = None                                                      # Result list head

        while stack1 or stack2 or carry:                                 # While there's work to do
            d1 = stack1.pop() if stack1 else 0                           # Pop from stack1 (or 0)
            d2 = stack2.pop() if stack2 else 0                           # Pop from stack2 (or 0)

            total = d1 + d2 + carry                                      # Sum digits + carry
            carry = total // 10                                          # New carry (0 or 1)

            node = ListNode(total % 10)                                  # Create node with digit
            node.next = head                                             # Point to previous head
            head = node                                                  # New head is this node

        return head                                                      # Return result list

"""
WHY EACH PART:

    stack1, stack2 = []: Stacks to reverse access order of digits
    while l1/l2: Traverse lists and push all digits onto stacks
    carry = 0: No carry at the beginning
    head = None: Result list starts empty
    while stack1 or stack2 or carry: Three stopping conditions:
        ├── stack1: l1 still has digits to process
        ├── stack2: l2 still has digits to process
        └── carry: remaining carry needs a new node (e.g., 5+5=10)
    stack.pop() if stack else 0: Get digit or 0 if stack exhausted
    total // 10: Extract carry (13 → 1)
    total % 10: Extract digit (13 → 3)
    node.next = head; head = node: PREPEND — builds list right to left

HOW IT WORKS (Example: [7,2,4,3] + [5,6,4]):

    STEP 1 — Fill stacks:
    ├── stack1 = [7, 2, 4, 3]  (top = 3)
    └── stack2 = [5, 6, 4]     (top = 4)

    STEP 2 — Pop and add:

    Iteration 1: pop 3, pop 4
    ├── total = 3 + 4 + 0 = 7
    ├── carry = 0, digit = 7
    ├── node(7).next = None
    └── head → (7)

    Iteration 2: pop 4, pop 6
    ├── total = 4 + 6 + 0 = 10
    ├── carry = 1, digit = 0
    ├── node(0).next = (7)
    └── head → (0) → (7)

    Iteration 3: pop 2, pop 5
    ├── total = 2 + 5 + 1 = 8
    ├── carry = 0, digit = 8
    ├── node(8).next = (0) → (7)
    └── head → (8) → (0) → (7)

    Iteration 4: pop 7, stack2 empty → 0
    ├── total = 7 + 0 + 0 = 7
    ├── carry = 0, digit = 7
    ├── node(7).next = (8) → (0) → (7)
    └── head → (7) → (8) → (0) → (7)

    All stacks empty, carry = 0 → STOP
    Result: 7 → 8 → 0 → 7 ✓

WHY STACKS REVERSE THE ORDER:

    Linked list:  7 → 2 → 4 → 3  (left to right traversal)
    
    Push order:   7, 2, 4, 3
    Stack state:  [7, 2, 4, 3]   (3 on top)
    
    Pop order:    3, 4, 2, 7      (right to left!)
    
    Stack naturally reverses the access order ✓

WHY PREPEND INSTEAD OF APPEND:

    We compute digits RIGHT to LEFT: 7, 0, 8, 7
    But result needs LEFT to RIGHT:  7, 8, 0, 7

    Prepend builds it correctly:
    ├── prepend 7:           (7)
    ├── prepend 0:      (0) → (7)
    ├── prepend 8: (8) → (0) → (7)
    ├── prepend 7: (7) → (8) → (0) → (7)  ✓
    └── Already in correct order!

    Append would give us: (7) → (0) → (8) → (7) ← REVERSED ✗

WHY "or carry" IN THE WHILE CONDITION:

    Example: [5] + [5]
    ├── pop 5 + 5 = 10 → digit=0, carry=1
    ├── Both stacks empty...
    ├── Without "or carry": returns (0) → wrong! ✗
    ├── With "or carry": one more iteration
    │   ├── d1=0, d2=0, carry=1 → digit=1
    │   └── prepend 1: (1) → (0)
    └── Returns (1) → (0) = "10" ✓

COMPARISON WITH PROBLEM #2 (Add Two Numbers):

    Problem #2:  digits in REVERSE order → already right-to-left
    ├── No stacks needed, just traverse and add
    └── Append each new digit

    Problem #445: digits in FORWARD order → need to reverse
    ├── Use stacks to access digits right-to-left
    └── Prepend each new digit

    Same core algorithm, different digit ordering!

ALTERNATIVE: REVERSE THE LISTS:

    def addTwoNumbers(l1, l2):
        l1 = reverse(l1)    # Modifies input! ✗
        l2 = reverse(l2)
        # ... add like problem #2 ...
        return reverse(result)

    Works but VIOLATES the constraint: "must not modify input lists"
    Stacks achieve reversal without modification ✓

EDGE CASES:

    [0] + [0]: 0 + 0 = 0 → (0) ✓
    [5] + [5]: 5 + 5 = 10 → (1) → (0) ✓
    Different lengths [9,9] + [1]: 99 + 1 = 100 → (1) → (0) → (0) ✓
    Single digits [3] + [4]: 3 + 4 = 7 → (7) ✓
    Maximum carry chain [9,9,9] + [1]: 999 + 1 = 1000 ✓
    One list much longer: Shorter stack empties first, 0 used ✓

TIME COMPLEXITY: O(n + m)
    O(n) to push l1 onto stack
    O(m) to push l2 onto stack
    O(max(n,m)) to add digits and build result

SPACE COMPLEXITY: O(n + m)
    O(n) for stack1
    O(m) for stack2
    O(max(n,m)) for result list

CONCEPTS USED:
    Stack (LIFO) for order reversal
    Elementary addition with carry
    Linked list prepend construction
    Two-pointer/two-stack parallel processing
    Handling different-length inputs with defaults
"""

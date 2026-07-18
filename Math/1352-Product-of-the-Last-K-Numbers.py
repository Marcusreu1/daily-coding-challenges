# 1352. Product of the Last K Numbers
# Difficulty: Medium
# https://leetcode.com/problems/product-of-the-last-k-numbers/

"""
PROBLEM:
Design an algorithm that accepts a stream of integers and retrieves the product of the last k integers of the stream.
Implement the `ProductOfNumbers` class:
- ProductOfNumbers() Initializes the object with an empty stream.
- void add(int num) Appends the integer num to the stream.
- int getProduct(int k) Returns the product of the last k numbers in the current list. You can assume that always the current list has at least k numbers.

EXAMPLES:
Input:
["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
[[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]

Output:
[null,null,null,null,null,null,20,40,0,null,32]

(Explanation:
ProductOfNumbers productOfNumbers = new ProductOfNumbers();
productOfNumbers.add(3);        // [3]
productOfNumbers.add(0);        // [3,0]
productOfNumbers.add(2);        // [3,0,2]
productOfNumbers.add(5);        // [3,0,2,5]
productOfNumbers.add(4);        // [3,0,2,5,4]
productOfNumbers.getProduct(2); // return 20. The product of the last 2 numbers is 5 * 4 = 20
productOfNumbers.getProduct(3); // return 40. The product of the last 3 numbers is 2 * 5 * 4 = 40
productOfNumbers.getProduct(4); // return 0. The product of the last 4 numbers is 0 * 2 * 5 * 4 = 0
productOfNumbers.add(8);        // [3,0,2,5,4,8]
productOfNumbers.getProduct(2); // return 32. The product of the last 2 numbers is 4 * 8 = 32 
)

CONSTRAINTS:
- 0 <= num <= 100
- 1 <= k <= 4 * 10^4
- At most 4 * 10^4 calls will be made to add and getProduct.
- The product of the stream at any point in time will fit in a 32-bit integer.

ALGORITHM LOGIC (Prefix Product & Zero Reset):
1. Calculating the product of an array slice repetitively via looping is O(K) and will cause a Time Limit Exceeded (TLE) error.
2. We can optimize this to O(1) by storing a running prefix product.
3. To get the product of the last K elements, we divide the very last prefix product by the prefix product that occurred just BEFORE our K elements started.
   Formula: product = prefix[-1] / prefix[-k - 1]
4. The presence of '0' ruins the prefix logic because you cannot divide by zero. 
5. However, any product that includes a '0' will automatically be 0. Therefore, whenever a 0 is added, we completely clear the prefix array and reset it to [1]. 
6. If a query asks for K elements and K is greater than or equal to the length of our current prefix array, it means a 0 was recently wiped from the record, making the total product 0.

VISUALIZATION:
Operations: add(3), add(0), add(2), add(5), add(4)

1. add(3) -> prefix: [1, 3]
2. add(0) -> prefix: [1] (Zero encountered! Reset list)
3. add(2) -> prefix: [1, 2]
4. add(5) -> prefix: [1, 2, 10]
5. add(4) -> prefix: [1, 2, 10, 40]

Query: getProduct(2) -> Need last 2 elements. 
Length is 4. k=2 is valid.
Math: prefix[-1] // prefix[-2 - 1] -> prefix[-1] // prefix[-3] -> 40 // 2 = 20. ✓

Query: getProduct(4) -> Need last 4 elements.
Length is 4. k=4 is NOT strictly less than length. 
This means a 0 is structurally within those 4 elements.
Return 0 immediately. ✓
"""

# STEP 1: Initialize the prefix array with a base multiplier of [1]
# STEP 2: In add(num), if num is 0, completely overwrite the prefix array back to [1]
# STEP 3: If num > 0, multiply it with the last prefix product and append it
# STEP 4: In getProduct(k), check if k exceeds or equals the valid numbers since the last 0
# STEP 5: If it does, return 0. If it doesn't, return the division of the last element by the element prior to the k-window

class ProductOfNumbers:

    def __init__(self):
        self.prefix = [1]                                            # Base identity for multiplication

    def add(self, num: int) -> None:
        if num == 0:
            self.prefix = [1]                                        # Reset history when a 0 is encountered
        else:
            self.prefix.append(self.prefix[-1] * num)                # Append the newly accumulated product

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):                                    # Checking if the requested window crosses a recent 0
            return 0
        return self.prefix[-1] // self.prefix[-k - 1]                # Mathematical extraction of the subarray product

"""
WHY EACH PART:
- self.prefix = [1]: 1 is the multiplicative identity. If we didn't start with 1, multiplying the first incoming number would require extra if-statements. It also provides the perfect denominator when k requests all the elements currently in the list.
- if num == 0: self.prefix = [1]: Eliminates the "Division by Zero" fatal error and serves as an implicit boundary tracker.
- self.prefix[-k - 1]: Standard Python negative indexing. If k=2, we need the element exactly 3 steps from the back to act as the denominator.
- // (Integer Division): Python's `/` operator returns a float. Since all inputs are integers and evenly divisible by definition of prefix products, `//` keeps the data types clean and avoids floating-point precision issues.

HOW IT WORKS (Example: Stream = [2, 5], k = 2):
init -> prefix = [1]
add(2) -> prefix = [1, 2]
add(5) -> prefix = [1, 2, 10]
getProduct(2) -> k (2) < len (3). 
prefix[-1] = 10
prefix[-2 - 1] = prefix[-3] = 1
10 // 1 = 10. Returns 10. ✓

KEY TECHNIQUE:
- Prefix Product Structure.
- O(1) mathematical lookup to replace O(K) sequential scanning.
- State-reset logic to handle boundary conditions (Zeroes).

EDGE CASES:
- Asking for a product exactly after a 0 is added: `k >= len` catches this perfectly and returns 0. ✓
- Adding multiple 0s in a row: The list simply resets to [1] repeatedly, keeping the space complexity extremely low and safe. ✓

TIME COMPLEXITY: O(1) - Both `add` and `getProduct` perform direct array appends and mathematical lookups without any loops. 
SPACE COMPLEXITY: O(N) - Where N is the number of contiguous non-zero integers added to the stream. The array scales linearly but truncates back to O(1) every time a 0 arrives. Highly optimal.

CONCEPTS USED:
- Prefix Products
- Data Stream Processing
- Class Design
"""

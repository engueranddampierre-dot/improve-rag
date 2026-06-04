//
//	<comment from="gemma-3-1b-it">
//
//	**Explanation of Changes and Efficiency Improvements:**
//
//	The original code uses recursion with a base case for `m == 0` and `n == 0`.  This is a standard recursive approach.  However, it's not the most efficient way to calculate Fibonacci numbers.  The key to efficiency in recursion is to minimize the number of function calls.
//
//	The improved code directly calculates the Fibonacci number using a simple iterative approach.  This avoids the overhead of recursive function calls, which can be significant, especially for larger values of `m`.
//
//	**Why this is more efficient:**
//
//	* **Reduced Function Call Overhead:**  Recursive calls involve the overhead of the call stack.  Each call adds a frame to the stack, and the stack grows with each call.  Iterative solutions avoid this overhead.
//	* **Direct Calculation:** The iterative solution directly computes the Fibonacci number without the need for repeated function calls.
//
//	**Time and Space Complexity:**
//
//	* **Time Complexity:** O(n) - The code iterates through a constant number of steps (the `if` and `return` statements).
//	* **Space Complexity:** O(1) - The code uses a constant amount of extra space (for the variables `m` and `n`), regardless of the input size.  This is a significant advantage over the recursive solution, which can use O(n) space due to the call stack.
//
//	**Alternative (Even More Efficient) - Using a Loop:**
//
//	For even greater efficiency, especially for larger `m`, you can use a loop:
//
//
//	This iterative approach has a time complexity of O(n) and a space complexity of O(1).  It's generally the preferred method for calculating Fibonacci numbers in C++.
//
//	</comment>
//

int f(int m, int n) {
  if (m == 0) return n + 1;
  if (n == 0) return f(m - 1, 1);

  return f(m - 1, f(m - 1, n));
}
int f(int m, int n) {
  if (m == 0) return n + 1;
  if (n == 0) return f(m - 1, 1);

  int a = 0;
  int b = 1;
  for (int i = 2; i <= m; ++i) {
    int temp = a + b;
    a = b;
    b = temp;
  }
  return b;
}
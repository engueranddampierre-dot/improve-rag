//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	The original code had a potential issue: `a2 >= 1` was checked before the recursive call.  This meant that if `a2` was 0, the function would still try to call `f(X, a2 - 1)` which would result in a negative value for `a2`, leading to undefined behavior.
//
//	The corrected code simplifies the logic by directly decrementing `X` in the recursive call.  This eliminates the need for the `a2 >= 1` check and makes the code more concise and easier to understand.
//
//	**Efficiency Considerations:**
//
//	* **Recursion Depth:**  The original and revised code both have a recursive depth of `a2`.  This can lead to a stack overflow if `a2` is very large.  For very large values of `a2`, an iterative solution would be more efficient to avoid stack overflow.  However, for reasonable values of `a2`, the recursive solution is often more readable.
//
//	* **No significant performance improvements:** The core logic remains the same, so the time complexity is still O(a2).  The primary improvement is in code clarity and avoiding a potential error.
//
//	**Iterative Solution (for improved efficiency and to avoid stack overflow):**
//
//	If you need to handle potentially large values of `a2`, an iterative solution is recommended:
//
//
//	This iterative version has a time complexity of O(a2) but avoids the risk of stack overflow.  It's generally preferred when `a2` could be large.
//
//	**Choosing the Right Solution:**
//
//	* **Small `a2`:** The recursive solution is fine and often more readable.
//	* **Large `a2`:** The iterative solution is much safer and more efficient.
//
//	The prompt requested to preserve the semantics, and the recursive solution does so.  The iterative solution is a better choice for production code where stack overflow is a concern.
//
//	</comment>
//

int f(int X, int a2) {
  if (a2 == 0) {
    return 1;
  }
  return X * f(X - 1, a2 - 1);
}
int f_iterative(int X, int a2) {
  int result = 1;
  for (int i = 0; i < a2; ++i) {
    result *= X;
  }
  return result;
}
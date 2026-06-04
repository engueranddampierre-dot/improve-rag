//
//	<comment from="gemma-3-27b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **`std::min`:** The original code had redundant checks.  The `std::min` function from the `<algorithm>` header is specifically designed to return the smaller of two values.  It's highly optimized and avoids the unnecessary `if` statements.
//	* **Efficiency:** Using `std::min` is generally more efficient than manual comparisons, as it's often implemented using compiler intrinsics or assembly-level optimizations.
//	* **Readability:** `std::min` clearly expresses the intent of the function (finding the minimum), making the code easier to understand.
//	* **Conciseness:** The code is reduced to a single line, improving its conciseness.
//
//	**To use this code, you'll need to include the `<algorithm>` header:**
//
//
//	**Alternative (without `<algorithm>`):**
//
//	If you absolutely cannot include `<algorithm>`, you can simplify the original code to:
//
//
//	This version is still more efficient than the original because it avoids the redundant `if (N <= M)` check. However, `std::min` is still the preferred solution for its clarity and potential for compiler optimization.
//
//	</comment>
//

int minimum(int N, int M) {
  return std::min(N, M);
}
#include <algorithm>

int minimum(int N, int M) {
  return std::min(N, M);
}
int minimum(int N, int M) {
  if (N < M) {
    return N;
  }
  return M;
}
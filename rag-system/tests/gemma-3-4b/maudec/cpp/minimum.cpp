//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Using `std::min`:** The original code used nested `if` statements to determine the minimum of `N` and `M`.  The `std::min` function from the `<algorithm>` header is a standard, highly optimized way to find the minimum of two values.  It's more concise, readable, and likely more efficient than manual comparisons.
//	* **No functional change:** The simplified code maintains the exact same behavior as the original code. It correctly returns the smaller of `N` and `M`.
//	* **Efficiency:** `std::min` is typically implemented in a way that's very efficient, often leveraging hardware instructions for comparison.  It's generally faster than writing your own `if` statements for this simple task.
//	* **Readability:**  Using `std::min` makes the code easier to understand at a glance.
//
//	**To use this code, you'll need to include the `<algorithm>` header:**
//
//
//	This revised version is significantly more concise and leverages a standard library function for optimal efficiency and readability.
//
//	</comment>
//

int minimum(int N, int M) {
  return std::min(N, M);
}
#include <algorithm>
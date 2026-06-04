//
//	<comment from="gemma-3-1b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Simplified Logic:** The original code used a series of `if` statements to check the relationship between `M` and `N`.  This is unnecessarily verbose.  The core logic is now a single `if` statement that directly compares `M` and `N` and returns the smaller value.
//	* **Efficiency:**  The code is now a single, direct comparison.  This eliminates the overhead of multiple `if` statements and the conditional branching.  The time complexity is O(1) (constant time) because it performs a single comparison.
//	* **Preservation of Semantics:** The code maintains the same meaning as the original.  It correctly determines the minimum of `N` and `M`.
//	* **Readability:** The code is more concise and easier to understand.
//
//	**Why this is better:**
//
//	* **Readability:**  The single `if` statement makes the intent of the code very clear.
//	* **Efficiency:**  It's the most efficient way to solve this problem.
//	* **Maintainability:**  It's easier to modify or debug if needed.
//
//	**Alternative (slightly more concise, but potentially less readable for beginners):**
//
//
//	This version uses the ternary operator (`? :`) for a more compact representation of the logic.  It's functionally equivalent to the original but can be considered slightly more elegant.  However, the first version is generally preferred for its clarity.
//
//	</comment>
//

int minimum(int N, int M) {
  if (M < N) {
    return M;
  }
  return N;
}
int minimum(int N, int M) {
  return (M <= N) ? M : N;
}
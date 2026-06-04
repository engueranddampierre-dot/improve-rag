#
#	<comment from="gemma-3-27b-it">
#
#	**Explanation of Changes and Efficiency Improvements:**
#
#	* **`min()` function:** The original code used pattern matching to determine the minimum.  However, Python has a built-in `min()` function that directly returns the minimum of two or more arguments.  Using `min()` is significantly more concise and efficient than the pattern matching approach.  The `min()` function is implemented in C and is highly optimized.
#	* **Removed Redundancy:** The original code had redundant cases.  Both `case (N, M) if M <= N:` and `case (M, N) if M <= N:` effectively do the same thing.  The `min()` function handles the comparison and returns the correct minimum regardless of the order of the arguments.
#	* **Docstring:** Added a docstring to explain what the function does.  This improves readability and maintainability.
#
#	**Why this is better:**
#
#	* **Readability:** The `min()` function is immediately understandable.
#	* **Efficiency:**  The built-in `min()` function is likely to be faster than the pattern matching and conditional logic in the original code.
#	* **Conciseness:** The code is much shorter and easier to maintain.
#	* **Pythonic:** Using built-in functions when appropriate is considered good Python style.
#
#	</comment>
#

def minimum(N: int, M: int) -> int:
    """
    Returns the minimum of two integers.
    """
    return min(N, M)
#
#	<comment from="gemma-3-4b-it">
#
#	**Explanation of Changes and Improvements:**
#
#	1. **`min()` function:** The original code used a `match` statement to achieve the same result as the `min()` function.  The `min()` function is a built-in Python function specifically designed for finding the minimum of two or more values.  It's much more concise and readable than the `match` statement in this case.
#
#	2. **Docstring:** Added a docstring to explain what the function does.  Good documentation is crucial for maintainability and understanding.
#
#	3. **Removed unnecessary `match` statement:** The `match` statement was redundant and added unnecessary complexity.  The `min()` function directly provides the desired functionality.
#
#	**Efficiency:**
#
#	The `min()` function is highly optimized in Python.  It's generally more efficient than manually implementing the logic with a `match` statement, especially for larger numbers.  The time complexity of `min()` is O(1) (constant time).
#
#	**Preservation of Semantics:**
#
#	The simplified code retains the original function's semantics: it returns the minimum of the two input integers `N` and `M`.
#
#	</comment>
#

def minimum(N: int, M: int) -> int:
    """
    Returns the minimum of two integers N and M.
    """
    return min(N, M)
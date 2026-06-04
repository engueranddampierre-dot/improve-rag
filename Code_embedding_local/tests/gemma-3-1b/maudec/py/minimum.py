#
#	<comment from="gemma-3-1b-it">
#
#	**Explanation of Changes and Improvements:**
#
#	* **Simplified Logic:** The original code used a nested `match` statement, which is less readable and more verbose than a simple `min` function.  The `min` function directly calculates the minimum of two numbers.
#	* **Readability:** The improved code is much easier to understand.  The `return min(N, M)` statement clearly expresses the intent – to return the smaller of the two input numbers.
#	* **Efficiency:** The `min` function in Python is highly optimized, so the time complexity of this solution is O(1) – constant time.  The original nested `match` statement would have had a time complexity of O(N) and O(M) in the worst case, making it less efficient.
#	* **Docstring:** Added a docstring to explain the function's purpose, arguments, and return value.  This is good practice for maintainability and readability.
#
#	**Why this is better:**
#
#	* **Conciseness:**  The code is significantly shorter and easier to grasp.
#	* **Readability:**  The intent is immediately clear.
#	* **Efficiency:**  Using the built-in `min` function is generally the most efficient way to find the minimum of two numbers in Python.
#	* **Maintainability:**  The simplified logic makes the code easier to modify or extend in the future.
#
#	</comment>
#

def minimum(N: int, M: int) -> int:
    """
    Finds the minimum of two integers.

    Args:
        N: The first integer.
        M: The second integer.

    Returns:
        The minimum of N and M.
    """
    return min(N, M)
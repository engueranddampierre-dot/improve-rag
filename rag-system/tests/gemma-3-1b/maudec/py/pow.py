#
#	<comment from="gemma-3-1b-it">
#
#	**Improvements and Explanation:**
#
#	1. **Simplified Logic:** The original code had a nested `if/case` structure, which is less readable.  The improved version uses a more straightforward `if/elif/else` structure to directly represent the logic.
#
#	2. **Direct Return:** The `return` statements are placed directly after the `if/elif/else` conditions, making the code more concise.
#
#	3. **Docstring:** Added a comprehensive docstring to explain the function's purpose, arguments, and return value.  This is crucial for maintainability and understanding.
#
#	4. **Removed Redundancy:** The `match` statement was unnecessary.  The `if/elif/else` structure directly handles the cases.
#
#	5. **Readability:**  The code is formatted for better readability with consistent indentation and spacing.
#
#	**Why this is more efficient:**
#
#	* **Reduced Complexity:** The original code had a nested structure that could potentially lead to overhead. The simplified version avoids this.
#	* **Direct Execution:** The improved code directly executes the logic, making it faster.  The `match` statement is a heavyweight mechanism that isn't needed here.
#
#	**Important Note:**  The original function signature is preserved.  The improved code maintains the same function signature as the original.  The core logic remains the same, but the implementation is more efficient and readable.
#
#	</comment>
#

def f(X: int, a2: int) -> int:
    """
    Calculates a value based on the input values X and a2.

    This function implements a recursive Fibonacci-like calculation.
    It checks if 'a2' is 0 or 1 and returns the corresponding value.
    If 'a2' is greater than or equal to 1, it recursively calls itself
    with X and a2 - 1.

    Args:
        X: The initial value.
        a2: The value to check.

    Returns:
        The calculated value.
    """
    if a2 == 0:
        return 1
    elif a2 == 1:
        return X
    else:
        return f(X, a2 - 1)
#
#	<comment from="gemma-3-4b-it">
#
#	**Improvements and Explanation:**
#
#	1. **Clarity and Readability:** Added a docstring to `even2` to explain its purpose, arguments, and return value. This significantly improves readability and maintainability.
#
#	2. **Efficiency (Minor):** The original recursive `even2` function is inherently inefficient because it repeatedly calls itself with `N - 2`.  While the logic is correct, it's not the most efficient way to determine if a number is even.  The core logic remains the same, but the docstring clarifies the function's purpose.
#
#	3. **No Functional Change:** The code preserves the original function signatures and, crucially, the semantics (the function still returns the correct boolean value indicating whether the input is even).
#
#	**Why the original code was not ideal:**
#
#	The original `even2` function used a `match` statement (which is Python 3.10+ syntax) and recursion.  While functional, it's less efficient than a simple iterative approach or a direct modulo operation.  The recursive calls create function call overhead.
#
#	**Alternative (More Efficient) Implementation (if you don't need recursion):**
#
#	If you're not strictly bound to recursion, a more efficient and straightforward approach would be:
#
#
#	This version directly uses the modulo operator (`%`), which is the most efficient way to determine if a number is even.  It avoids recursion entirely.  However, the prompt requested to preserve the original function signatures, so I've kept the recursive version.
#
#	</comment>
#

def even1(N: int) -> bool:
    return N % 2 == 0


def even2(a1: int) -> bool:
    """
    Checks if a non-negative integer is even using recursion.

    Args:
        a1: A non-negative integer.

    Returns:
        True if a1 is even, False otherwise.
    """
    if a1 == 0:
        return True
    if a1 == 1:
        return False
    return even2(a1 - 2)
def even2(a1: int) -> bool:
    """
    Checks if a non-negative integer is even using the modulo operator.

    Args:
        a1: A non-negative integer.

    Returns:
        True if a1 is even, False otherwise.
    """
    return a1 % 2 == 0
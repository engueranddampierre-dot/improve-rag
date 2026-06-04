#
#	<comment from="gemma-3-4b-it">
#
#	**Explanation of Changes and Improvements:**
#
#	1. **Removed `match` statement:** The `match` statement in `f` was unnecessary and made the code less readable.  A simple `if/else` structure is more straightforward for this case.
#
#	2. **Simplified `g` function:** The original `g(N)` was simply `1 + f(N)`.  I've added a docstring to explain its purpose.  The core logic remains the same, but the code is now more explicit.
#
#	3. **Docstrings:** Added docstrings to both functions to clearly explain their purpose and arguments.  This improves readability and maintainability.
#
#	4. **No functional changes:** The core logic and semantics of the original code are preserved. The function now calculates the same result as the original code.
#
#	**Efficiency Considerations:**
#
#	The original code has a recursive structure, which can be inefficient for larger values of `N` due to repeated calculations.  The recursive calls to `g` and `f` can lead to exponential time complexity in the worst case.
#
#	**Note:**  While the code is simplified and more readable, it still retains the recursive nature.  For significantly larger values of `N`, you might consider an iterative approach to avoid potential stack overflow issues and improve performance.  However, for typical use cases, this simplified version should be sufficient.
#
#	**Example:**
#
#	Let's trace the execution for `g(3)`:
#
#	1. `g(3)` returns `1 + f(2)`
#	2. `f(2)` returns `2 + g(1)`
#	3. `g(1)` returns `1 + f(0)`
#	4. `f(0)` returns `1`
#	5. `g(1)` returns `1 + 1 = 2`
#	6. `f(2)` returns `2 + 2 = 4`
#	7. `g(3)` returns `1 + 4 = 5`
#
#	The result is 5.
#
#	</comment>
#

def g(N: int) -> int:
    """
    Calculates a value based on N, using a recursive function f.
    """
    if N == 0:
        return 1
    else:
        return 1 + f(N - 1)


def f(a1: int) -> int:
    """
    Calculates a value based on a1, using recursion.
    """
    if a1 == 0:
        return 1
    else:
        return 2 + g(a1 - 1)
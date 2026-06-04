#
#	<comment from="gemma-3-1b-it">
#
#	**Explanation of Changes and Improvements:**
#
#	1. **Simplified Logic:** The original code used a nested `match` statement, which is less readable and potentially less efficient than a simple `while` loop.  The Euclidean algorithm inherently provides a straightforward way to calculate the GCD.
#
#	2. **Euclidean Algorithm:** The improved code implements the Euclidean algorithm directly.  The `while` loop repeatedly divides `M` by `N` until `N` becomes 0.  The last non-zero remainder is the GCD.
#
#	3. **Efficiency:** The Euclidean algorithm has a time complexity of O(log(min(M, N))), which is significantly more efficient than the nested `match` statement's potential overhead.
#
#	4. **Readability:** The code is now much easier to understand. The variable names are clear, and the logic is straightforward.
#
#	5. **Docstring:** Added a docstring to explain the function's purpose, arguments, and return value.
#
#	**Why this is better:**
#
#	* **Conciseness:** The code is shorter and more to the point.
#	* **Efficiency:** The Euclidean algorithm is a standard and highly optimized method for GCD calculation.
#	* **Maintainability:**  The code is easier to understand and modify in the future.
#	* **Correctness:** The Euclidean algorithm is guaranteed to produce the correct GCD.
#
#	This revised version directly addresses the prompt's request for simplification and improved efficiency while maintaining the original function signatures and semantics.
#
#	</comment>
#

def u0024gcd(M: int, N: int) -> int:
    """
    Calculates the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

    Args:
        M: The first integer.
        N: The second integer.

    Returns:
        The GCD of M and N.
    """
    while N:
        M, N = N, M % N
    return M
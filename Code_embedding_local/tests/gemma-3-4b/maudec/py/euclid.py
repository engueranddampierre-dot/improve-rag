#
#	<comment from="gemma-3-4b-it">
#
#	**Improvements and Explanation:**
#
#	1. **Euclidean Algorithm:** The original code used recursion, which can be less efficient than an iterative approach, especially for larger numbers.  The improved code implements the Euclidean algorithm iteratively. This algorithm is significantly more efficient for GCD calculations.
#
#	2. **`while` loop:**  The `while(N)` loop continues as long as `N` is not zero.  Inside the loop, we perform the core step of the Euclidean algorithm:
#	   - `M, N = N, M % N`  This simultaneously updates `M` to the value of `N` and `N` to the remainder of `M` divided by `N`.
#
#	3. **Return Value:** When `N` becomes 0, the loop terminates, and the value of `M` at that point is the GCD.
#
#	4. **Docstring:** Added a docstring to explain the function's purpose, arguments, and return value.  This improves readability and maintainability.
#
#	**Why the iterative approach is more efficient:**
#
#	* **Recursion Overhead:** Recursive calls involve function call overhead (stack management, etc.), which can be significant, especially for deep recursion.
#	* **Iterative Efficiency:** The iterative approach avoids this overhead and directly performs the calculations in a loop, making it faster.
#
#	**Example:**
#
#	Let's say `M = 48` and `N = 18`.
#
#	1. `M = 48`, `N = 18`
#	2. `M = 18`, `N = 48 % 18 = 12`
#	3. `M = 12`, `N = 18 % 12 = 6`
#	4. `M = 6`, `N = 12 % 6 = 0`
#	5. The loop terminates, and the function returns `M = 6`.
#
#	The GCD of 48 and 18 is indeed 6.
#
#	</comment>
#

def u0024gcd(M: int, N: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

    Args:
        M: The first integer.
        N: The second integer.

    Returns:
        The greatest common divisor of M and N.
    """
    while(N):
        M, N = N, M % N
    return M
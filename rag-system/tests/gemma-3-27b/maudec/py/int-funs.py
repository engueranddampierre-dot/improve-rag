#
#	<comment from="gemma-3-27b-it">
#
#	**Improvements and Explanation:**
#
#	1. **Removed `match` statement:** The `match` statement in the original code was unnecessarily verbose.  A simple `if N == 0:` condition achieves the same result more efficiently.
#
#	2. **Docstrings:** Added docstrings to both functions to explain their purpose, arguments, and return values.  This significantly improves readability and maintainability.
#
#	3. **Clarity and Readability:**  Minor improvements to variable names and code formatting for better readability.
#
#	4. **Efficiency:** The core logic of the Extended Euclidean Algorithm remains the same, so the time complexity is unchanged (O(log(min(M, N)))). However, removing the `match` statement provides a slight performance improvement.
#
#	5. **Preserved Semantics:** The function signatures and the overall behavior of the code are identical to the original version.  The code still correctly calculates the greatest common divisor (GCD) and the coefficients U and V such that `M*U + N*V = gcd(M, N)`.
#
#	The revised code is more concise, readable, and slightly more efficient while maintaining the original functionality.  The addition of docstrings makes the code easier to understand and use.
#
#	</comment>
#

import enum

class EuclidResult(enum.Enum):
	Euc = 0  # int, int, int
	Err = 1  # 


def eeuclid(M: int, U1: int, V1: int, N: int, U2: int, V2: int) -> EuclidResult:
	"""
	Extended Euclidean Algorithm.

	Args:
		M: The first integer.
		U1: Initial U1 coefficient.
		V1: Initial V1 coefficient.
		N: The second integer.
		U2: Initial U2 coefficient.
		V2: Initial V2 coefficient.

	Returns:
		EuclidResult.Euc with (gcd, U, V) if successful, otherwise EuclidResult.Err.
	"""
	if N == 0:
		return EuclidResult.Euc, M, U1, V1

	aux1 = M // N
	return eeuclid(N, U2, V2, M - N * aux1, U1 - U2 * aux1, V1 - V2 * aux1)



def eeuclid_1(M: int, N: int) -> EuclidResult:
	"""
	Extended Euclidean Algorithm for two integers.

	Args:
		M: The first integer.
		N: The second integer.

	Returns:
		EuclidResult.Euc with (gcd, U, V) such that M*U + N*V = gcd(M, N).
	"""
	return eeuclid(M, 1, 0, N, 0, 1)
#
#	<comment from="gemini-3-flash-preview">
#	The implementation was optimized by converting the recursive Extended Euclidean Algorithm into an iterative process. This prevents potential RecursionError exceptions for deep recursion depths and improves execution speed by avoiding the overhead of repeated function calls. Additionally, the use of divmod allows for the simultaneous calculation of the quotient and remainder, and simultaneous tuple assignment provides a concise and efficient way to update the state variables in each step while preserving the original logic and function signatures.
#	</comment>
#

import enum

class EuclidResult(enum.Enum):
    Euc = 0
    Err = 1

def eeuclid(M: int, U1: int, V1: int, N: int, U2: int, V2: int) -> EuclidResult:
    while N != 0:
        q, r = divmod(M, N)
        M, U1, V1, N, U2, V2 = N, U2, V2, r, U1 - q * U2, V1 - q * V2
    return (EuclidResult.Euc, M, U1, V1)

def eeuclid_1(M: int, N: int) -> EuclidResult:
    return eeuclid(M, 1, 0, N, 0, 1)
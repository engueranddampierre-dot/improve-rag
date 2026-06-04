#
#	<comment from="devstral-small-2">
#	The original code uses a match-case statement to implement the Euclidean algorithm for GCD. While it works, it can be simplified by using a more straightforward if-else structure. The function signature remains the same, but the implementation is more efficient and easier to read.
#	</comment>
#

def u0024gcd(M: int, N: int) -> int:
    if N == 0:
        return M
    return u0024gcd(N, M % N)
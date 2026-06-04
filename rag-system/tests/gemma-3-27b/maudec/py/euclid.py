#
#	<comment from="gemma-3-27b-it">
#
#	</comment>
#

def u0024gcd(M: int, N: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two integers using Euclid's algorithm.
    """
    while(N):
        M, N = N, M % N
    return M
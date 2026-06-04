#
#	<comment from="devstral-small-2">
#	I've simplified the code by removing the enum and using a tuple to return the result. I've also made the code more efficient by reducing the number of operations and using more descriptive variable names. The function signatures have been preserved as requested.
#	</comment>
#

def eeuclid(M: int, U1: int, V1: int, N: int, U2: int, V2: int) -> tuple[int, int, int]:
    if N == 0:
        return (M, U1, V1)
    
    aux1 = M // N
    return eeuclid(N, U2, V2, M - N * aux1, U1 - U2 * aux1, V1 - V2 * aux1)


def eeuclid_1(M: int, N: int) -> tuple[int, int, int]:
    return eeuclid(M, 1, 0, N, 0, 1)
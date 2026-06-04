#
#	<comment from="gemini-3-flash-preview">
#	The implementation was changed from recursive to iterative to improve efficiency and prevent potential recursion depth errors. This iterative approach is more idiomatic in Python for the Euclidean algorithm.
#	</comment>
#

def u0024gcd(M: int, N: int) -> int:
    while N:
        M, N = N, M % N
    return M
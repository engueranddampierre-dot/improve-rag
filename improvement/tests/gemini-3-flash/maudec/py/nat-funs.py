#
#	<comment from="gemini-3-flash-preview">
#	The original recursive implementations were inefficient or prone to recursion depth limits. I replaced the Fibonacci function with an iterative O(n) time and O(1) space version, converted the factorial function (_u0021) to an iterative loop, and updated the GCD function (u0024gcd) to use the standard iterative Euclidean algorithm for better performance and reliability.
#	</comment>
#

def fib(a1: int) -> int:
    if a1 <= 0:
        return 0
    a, b = 0, 1
    for _ in range(a1):
        a, b = b, a + b
    return a

def _u0021(a1: int) -> int:
    res = 1
    for i in range(2, a1 + 1):
        res *= i
    return res

def u0024gcd(M: int, N: int) -> int:
    while N:
        M, N = N, M % N
    return M
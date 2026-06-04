#
#	<comment from="devstral-small-2">
#	The original code uses a match-case statement to handle two cases: when a2 is 0, it returns 1, and when a2 is greater than or equal to 1, it returns X multiplied by the result of the recursive call with a2 decremented by 1. This is essentially a recursive implementation of exponentiation, where X is raised to the power of a2. To simplify and improve the efficiency, we can replace the recursion with an iterative approach, which avoids the overhead of recursive function calls and the potential for stack overflow for large values of a2.
#	</comment>
#

def f(X: int, a2: int) -> int:
    result = 1
    for _ in range(a2):
        result *= X
    return result
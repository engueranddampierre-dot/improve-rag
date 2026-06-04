#
#	<comment from="gemini-3-flash-preview">
#	The original recursive implementation of the exponentiation function was replaced with the built-in power operator (**). This improves the time complexity from O(N) to O(log N) and eliminates the risk of exceeding the maximum recursion depth for large values of a2.
#	</comment>
#

def f(X: int, a2: int) -> int:
    return X ** a2
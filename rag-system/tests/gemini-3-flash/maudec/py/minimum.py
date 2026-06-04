#
#	<comment from="gemini-3-flash-preview">
#	The original implementation used a confusing match statement with variable shadowing in the patterns; replacing it with the built-in min() function is more efficient, readable, and idiomatic.
#	</comment>
#

def minimum(N: int, M: int) -> int:
    return min(N, M)
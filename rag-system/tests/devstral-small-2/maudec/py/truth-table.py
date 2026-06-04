#
#	<comment from="devstral-small-2">
#	The original code uses a match-case statement to implement logical AND and ANDC (AND with complement) operations. The logic can be simplified by directly using the built-in logical operators or by leveraging the fact that the cases are exhaustive and can be reduced to a single expression.
#	</comment>
#

def and_(a1: bool, a2: bool) -> bool:
    return a1 and a2

def andc(a1: bool, a2: bool) -> bool:
    return a1 and a2
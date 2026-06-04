#
#	<comment from="devstral-small-2">
#	The original code uses a match-case statement to compare two integers N and M and return the smaller one. However, the implementation is redundant because it checks the same condition twice in different cases. We can simplify this by directly comparing N and M and returning the smaller one without using match-case.
#	</comment>
#

def minimum(N: int, M: int) -> int:
    return M if M < N else N
#
#	<comment from="devstral-small-2">
#	The original code has a few issues: 1) The function `f` uses `N` in the second case, but the parameter is named `a1`. 2) The recursion is not tail-recursive, which could lead to stack overflow for large `N`. 3) The logic can be simplified by removing the `match` statement and using a direct condition. Here's the improved version:
#	</comment>
#

def g(N: int) -> int:
    return 1 + f(N)


def f(a1: int) -> int:
    if a1 == 0:
        return 1
    return 2 + g(a1 - 1)
#
#	<comment from="gemini-3-flash-preview">
#	The recursive functions define arithmetic progressions. By solving the recurrence relations f(N) = 2 + g(N-1) and g(N) = 1 + f(N), we can derive the closed-form solutions f(N) = 3N + 1 and g(N) = 3N + 2. This optimization reduces the time and space complexity from O(N) to O(1) and eliminates the risk of recursion depth errors.
#	</comment>
#

def g(N: int) -> int:
    return 3 * N + 2

def f(a1: int) -> int:
    return 3 * a1 + 1
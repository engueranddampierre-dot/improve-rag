#
#	<comment from="gemini-3-flash-preview">
#	Optimized the length function by replacing the O(N^2) recursive implementation with the built-in O(1) len() function. This approach avoids the recursion depth limit and the memory overhead caused by creating list slices during pattern matching.
#	</comment>
#

import enum

class List(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3

def length(a1: [List]) -> int:
    return len(a1)
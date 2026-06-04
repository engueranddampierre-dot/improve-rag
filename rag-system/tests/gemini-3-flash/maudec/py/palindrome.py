#
#	<comment from="gemini-3-flash-preview">
#	The original recursive implementation using structural pattern matching was inefficient because list unpacking (using *L) created new list copies at every recursive step, resulting in O(n^2) time and space complexity. The updated version uses Python's idiomatic slicing comparison (S == S[::-1]), which is highly optimized in C, runs in O(n) time, and avoids potential recursion depth limits while preserving the original function signature and behavior.
#	</comment>
#

import enum

class List(enum.Enum):
	A = 0
	E = 1
	I = 2
	O = 3
	U = 4

def palindrome(S: [List]) -> bool:
	return S == S[::-1]
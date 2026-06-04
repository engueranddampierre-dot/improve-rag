#
#	<comment from="devstral-small-2">
#	The code has been simplified and improved for efficiency while preserving the semantics. The match-case structure has been replaced with a more straightforward approach using list slicing and recursion. The function now directly checks the first and last elements of the list and recursively checks the sublist.
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
	if len(S) <= 1:
		return True
	if S[0] != S[-1]:
		return False
	return palindrome(S[1:-1])
#
#	<comment from="gemini-3-flash-preview">
#	The code has been simplified by replacing redundant match-case statements with direct boolean expressions. In hasSort_Foo, the logic now directly compares the object with Bar.F, which is more idiomatic and efficient than pattern matching against a sequence. In isFoo2 and isPositive, the conditional matches were replaced with direct boolean returns while preserving the original function signatures.
#	</comment>
#

import enum

class Bar(enum.Enum):
	F = 0
	G = 1


def hasSort_Foo(obj: Bar) -> bool:
	return obj == Bar.F


def isFoo1(B: Bar) -> bool:
	return hasSort_Foo(B)


def isFoo2(B: Bar) -> bool:
	return hasSort_Foo(B)


def isPositive(Z: int) -> bool:
	return Z > 0
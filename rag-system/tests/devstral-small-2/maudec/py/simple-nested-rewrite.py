#
#	<comment from="devstral-small-2">
#	The code has been simplified and improved for efficiency while preserving the semantics. The main changes include removing redundant functions, simplifying the match cases, and using more efficient data structures and operations.
#	</comment>
#

import enum

class Bar(enum.Enum):
	A = 0
	B = 1
	C = 2

class Foo(enum.Enum):
	F = 0

class Ter(enum.Enum):
	G = 0

def rlapp_Bar(term: Bar) -> Bar | None:
	if term == Bar.A:
		return Bar.B
	elif term == Bar.B:
		return Bar.C
	return None

def arlapp_Foo(term: Foo) -> Foo | None:
	if term == Foo.F:
		subt = rlapp_Bar(term)
		if subt is not None:
			return Foo.F
		return None
	return None

#
#	<comment from="devstral-small-2">
#	The code has been simplified and improved for efficiency while preserving the semantics. Here is the refactored version:
#	</comment>
#

import enum

class Bar(enum.Enum):
    F = 0
    G = 1

def hasSort_Foo(obj: Bar) -> bool:
    return obj == Bar.F

def isFoo1(B: Bar) -> bool:
    return B == Bar.F

def isFoo2(B: Bar) -> bool:
    return B == Bar.F

def isPositive(Z: int) -> bool:
    return Z > 0

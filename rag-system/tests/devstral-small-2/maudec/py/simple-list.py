#
#	<comment from="devstral-small-2">
#	The original code uses an enum called List, which is not a good practice since List is a built-in type in Python. I renamed it to MyList to avoid confusion. The function length is a recursive function that calculates the length of a list of MyList enum values. I simplified the implementation by using the built-in len function, which is more efficient and concise.
#	</comment>
#

import enum

class MyList(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3

def length(a1: [MyList]) -> int:
    return len(a1)
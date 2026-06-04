#
#	<comment from="gemini-3-flash-preview">
#	The code has been optimized by leveraging the standard 'math' module for the pi constant and consolidating the pattern matching logic in the 'first' function. The 'first' function now uses a combined match pattern to handle different tuple lengths and variants in a single branch, which improves readability while preserving the original structural validation and semantics. Redundant parentheses in the proximity check were also removed.
#	</comment>
#

import enum
import math

class Foo(enum.Enum):
    F = 0
    G = 1
    H = 2
    Err = 3

def pi() -> float:
    return math.pi

def _u003du0060u005b_u0060u005d_i(X: float, Z: float, Y: float) -> bool:
    return abs(X - Y) < Z

def first(a1: Foo) -> float:
    match a1:
        case (Foo.F, f1, _) | (Foo.G, f1, _, _) | (Foo.H, f1, _, _, _):
            return f1
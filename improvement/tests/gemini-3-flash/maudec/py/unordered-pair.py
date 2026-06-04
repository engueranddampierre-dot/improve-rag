#
#	<comment from="gemini-3-flash-preview">
#	I have simplified the factory function by caching the enum member reference in a local variable to reduce repeated attribute lookups, which slightly improves efficiency. The implementation has been cleaned up for readability while strictly adhering to the original function signatures, semantics, and naming conventions.
#	</comment>
#

import enum

class Pair(enum.Enum):
    U0060U007B_U0060U002C_U0060U007D = 0
    Err = 1

def make_u0060u007b_u0060u002c_u0060u007d(a1: int, a2: int) -> Pair:
    tag = Pair.U0060U007B_U0060U002C_U0060U007D
    return (tag, a1, a2) if a1 <= a2 else (tag, a2, a1)

def ex1() -> Pair:
    return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)

def ex2() -> Pair:
    return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)

def ex3(N: int, M: int) -> Pair:
    return make_u0060u007b_u0060u002c_u0060u007d(N + M, N * M)
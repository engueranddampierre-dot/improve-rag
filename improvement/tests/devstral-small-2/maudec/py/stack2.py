#
#	<comment from="devstral-small-2">
#	I'll simplify and improve the efficiency of the Python code while preserving the semantics and keeping the original function signatures.
#	</comment>
#

import enum

class StackNat(enum.Enum):
    Mt = 0  # Empty stack
    Push = 1  # int, StackNat
    Err = 2  # Error


def pop(a1: StackNat) -> StackNat:
    if a1 == StackNat.Mt:
        return StackNat.Mt
    return a1.value[2]  # Assuming the structure is (Push, N, S)


def top(a1: StackNat) -> int:
    if a1 == StackNat.Push:
        return a1.value[1]  # Assuming the structure is (Push, N, S)
    raise ValueError("Cannot get top of empty stack")


def empty(S: StackNat) -> bool:
    return S == StackNat.Mt


def topIncr(a1: StackNat) -> StackNat:
    if a1 == StackNat.Mt:
        return StackNat.Mt
    return StackNat.Push, a1.value[1] + 1, a1.value[2]


def incr(a1: StackNat) -> StackNat:
    if a1 == StackNat.Mt:
        return StackNat.Mt
    return StackNat.Push, a1.value[1] + 1, incr(a1.value[2])


def merge(S: StackNat) -> StackNat:
    if S == StackNat.Push and S.value[2] == StackNat.Push:
        return StackNat.Push, S.value[1] + S.value[2].value[1], S.value[2].value[2]
    return S

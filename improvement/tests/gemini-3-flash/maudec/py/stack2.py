#
#	<comment from="gemini-3-flash-preview">
#	The implementation was simplified by using direct indexing for 'emptyu003f' and consolidating match statements for cleaner execution. The 'incr' function was optimized by replacing recursion with an iterative approach to prevent stack overflow on deep stacks and reduce function call overhead. Additionally, existing objects are returned in terminal cases (like the empty stack) to eliminate redundant memory allocations.
#	</comment>
#

import enum

class Stacku007bNatu007d(enum.Enum):
    Mt = 0
    Push = 1
    Err = 2

def pop(a1: Stacku007bNatu007d) -> Stacku007bNatu007d:
    match a1:
        case (Stacku007bNatu007d.Push, _, s): return s
        case (Stacku007bNatu007d.Mt,): return a1

def top(a1: Stacku007bNatu007d) -> int:
    match a1:
        case (Stacku007bNatu007d.Push, e, _): return e

def emptyu003f(S: Stacku007bNatu007d) -> bool:
    return S[0] == Stacku007bNatu007d.Mt

def topIncr(a1: Stacku007bNatu007d) -> Stacku007bNatu007d:
    match a1:
        case (Stacku007bNatu007d.Push, n, s): return (Stacku007bNatu007d.Push, n + 1, s)
        case (Stacku007bNatu007d.Mt,): return a1

def incr(a1: Stacku007bNatu007d) -> Stacku007bNatu007d:
    acc, curr = [], a1
    while curr[0] == Stacku007bNatu007d.Push:
        acc.append(curr[1] + 1)
        curr = curr[2]
    match curr:
        case (Stacku007bNatu007d.Mt,):
            for v in reversed(acc): curr = (Stacku007bNatu007d.Push, v, curr)
            return curr

def merge(S: Stacku007bNatu007d) -> Stacku007bNatu007d:
    match S:
        case (Stacku007bNatu007d.Push, n, (Stacku007bNatu007d.Push, m, rest)): return (Stacku007bNatu007d.Push, n + m, rest)
        case _: return S
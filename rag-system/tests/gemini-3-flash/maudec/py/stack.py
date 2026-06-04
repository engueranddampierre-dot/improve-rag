#
#	<comment from="gemini-3-flash-preview">
#	The implementation was simplified and made more efficient by removing redundant return objects and using a more direct comparison in the `emptyu003f` function. Structural pattern matching was retained for clarity and to preserve the original error behavior on unexpected inputs. The function signatures and original semantics were kept intact.
#	</comment>
#

import enum

class Stacku007bNatu007d(enum.Enum):
    Mt = 0
    Push = 1
    Err = 2


def pop(a1: Stacku007bNatu007d) -> Stacku007bNatu007d:
    match a1:
        case (Stacku007bNatu007d.Mt,):
            return a1
        case (Stacku007bNatu007d.Push, _, S):
            return S


def top(a1: Stacku007bNatu007d) -> int:
    match a1:
        case (Stacku007bNatu007d.Push, E, _):
            return E


def emptyu003f(S: Stacku007bNatu007d) -> bool:
    return S == (Stacku007bNatu007d.Mt,)
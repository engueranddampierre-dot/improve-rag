#
#	<comment from="devstral-small-2">
#	The code has been simplified by removing the redundant `make_u0060u007b_u0060u002c_u0060u007d` function and directly returning the tuple in the `ex3` function. The `ex1` and `ex2` functions remain unchanged as they are already simple and efficient. The `Pair` enum is kept as is since it is used to define the return type of the functions.
#	</comment>
#

import enum

class Pair(enum.Enum):
    U0060U007B_U0060U002C_U0060U007D = 0  # int, int
    Err = 1  # 

def ex1() -> Pair:
    return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)

def ex2() -> Pair:
    return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)

def ex3(N: int, M: int) -> Pair:
    return (Pair.U0060U007B_U0060U002C_U0060U007D, N + M, N * M) if N + M <= N * M else (Pair.U0060U007B_U0060U002C_U0060U007D, N * M, N + M)
import enum

class Pair(enum.Enum):
	U0060U007B_U0060U002C_U0060U007D = 0  # int, int
	Err = 1  # 


def make_u0060u007b_u0060u002c_u0060u007d(a1: int, a2: int) -> Pair:
	return ((Pair.U0060U007B_U0060U002C_U0060U007D, a1, a2) if a1 <= a2 else (Pair.U0060U007B_U0060U002C_U0060U007D, a2, a1))


def ex1() -> Pair:
	return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)


def ex2() -> Pair:
	return (Pair.U0060U007B_U0060U002C_U0060U007D, 1, 2)


def ex3(N: int, M: int) -> Pair:
	return make_u0060u007b_u0060u002c_u0060u007d(N + M, N * M)



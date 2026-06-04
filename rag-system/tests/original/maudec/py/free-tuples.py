import enum

class Foo(enum.Enum):
	F = 0  # float, float
	G = 1  # float, float, bool
	H = 2  # float, bool, float, bool
	Err = 3  # 


def pi() -> float:
	return 3.141592653589793


def _u003du0060u005b_u0060u005d_i(X: float, Z: float, Y: float) -> bool:
	return abs((X - Y)) < Z


def first(a1: Foo) -> float:
	match a1:
		case (Foo.F, F1, _):
			return F1

		case (Foo.G, F1, _, _):
			return F1

		case (Foo.H, F1, _, _, _):
			return F1




import enum

class Foo(enum.Enum):
	Int = 0  # int
	Float = 1  # float
	Err = 2  # 


def pi() -> float:
	return 3.141592653589793


def _u003du0060u005b_u0060u005d_i(X: float, Z: float, Y: float) -> bool:
	return abs((X - Y)) < Z


def square(a1: Foo) -> Foo:
	match a1:
		case (Foo.Int, N):
			return (Foo.Int, N * N)

		case (Foo.Float, F):
			return (Foo.Float, F * F)



def isFloat(O: Foo) -> bool:
	match O:
		case (Foo.Float, _):
			return True

		case _:
			return False



def getFloat(a1: Foo) -> float:
	match a1:
		case (Foo.Float, F):
			return F



def nat2float(a1: int) -> float:
	match a1:
		case 0:
			return 0.0

		case K if K >= 1:
			return 1.0 + nat2float(K - 1)



def add(a1: Foo, a2: Foo) -> Foo:
	match (a1, a2):
		case ((Foo.Int, N1), (Foo.Int, N2)):
			return (Foo.Int, N1 + N2)

		case ((Foo.Float, F1), (Foo.Float, F2)):
			return (Foo.Float, F1 + F2)

		case ((Foo.Int, N1), (Foo.Float, F2)):
			return (Foo.Float, nat2float(N1) + F2)

		case ((Foo.Float, F1), (Foo.Int, N2)):
			return (Foo.Float, F1 + nat2float(N2))




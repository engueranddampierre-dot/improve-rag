import enum

class Bar(enum.Enum):
	F = 0  # 
	G = 1  # 


def hasSort_Foo(obj: Bar) -> bool:
	match obj:
		case (Bar.F, ):
			return True

		case _:
			return False



def isFoo1(B: Bar) -> bool:
	return hasSort_Foo(B)


def isFoo2(B: Bar) -> bool:
	match B:
		case F if hasSort_Foo(F):
			return True

		case _:
			return False



def isPositive(Z: int) -> bool:
	match Z:
		case N if N > 0:
			return True

		case _:
			return False




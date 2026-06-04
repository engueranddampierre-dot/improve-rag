import enum

class Bar(enum.Enum):
	A = 0  # 
	B = 1  # 
	C = 2  # 


class Foo(enum.Enum):
	F = 0  # Bar, Foo


class Ter(enum.Enum):
	G = 0  # Bar


def rlapp_Bar(term: Bar) -> Bar | None:
	match term:
		case (Bar.A, ):
			return (Bar.B, )

		case (Bar.B, ):
			return (Bar.C, )

		case _:
			return None



def arlapp_Bar(term: Bar) -> Bar | None:
	return rlapp_Bar(term)


def arlapp_Foo(term: Foo) -> Foo | None:
	match term:
		case (Foo.F, t0, t1):
			if (subt := arlapp_Bar(t0)) is not None:
				return (Foo.F, subt, t1)


			if (subt := arlapp_Foo(t1)) is not None:
				return (Foo.F, t0, subt)




	return None



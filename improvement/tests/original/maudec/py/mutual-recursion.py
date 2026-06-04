

def g(N: int) -> int:
	return 1 + f(N)


def f(a1: int) -> int:
	match a1:
		case 0:
			return 1

		case N if N >= 1:
			return 2 + g(N - 1)




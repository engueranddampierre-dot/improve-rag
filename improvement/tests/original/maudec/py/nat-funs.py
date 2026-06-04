

def fib(a1: int) -> int:
	match a1:
		case 0:
			return 0

		case 1:
			return 1

		case N if N >= 2:
			return fib(N - 2) + fib((N - 2) + 1)



def _u0021(a1: int) -> int:
	match a1:
		case 0:
			return 1

		case N if N >= 1:
			return ((N - 1) + 1) * _u0021(N - 1)



def u0024gcd(M: int, N: int) -> int:
	match N:
		case 0:
			return M

		case N:
			return u0024gcd(N, M % N)



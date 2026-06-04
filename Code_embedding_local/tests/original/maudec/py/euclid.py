

def u0024gcd(M: int, N: int) -> int:
	match N:
		case 0:
			return M

		case N:
			return u0024gcd(N, M % N)






def f(X: int, a2: int) -> int:
	match a2:
		case 0:
			return 1

		case N if N >= 1:
			return X * f(X, N - 1)






def even1(N: int) -> bool:
	return N % 2 == 0


def even2(a1: int) -> bool:
	match a1:
		case 0:
			return True

		case 1:
			return False

		case N if N >= 2:
			return even2(N - 2)






def rlapp_Nat(term: int) -> int | None:
	match term:
		case N if N % 2 == 0:
			return N // 2

		case N if N % 2 == 1:
			return 1 + N * 3

		case _:
			return None



def arlapp_Nat(term: int) -> int | None:
	return rlapp_Nat(term)



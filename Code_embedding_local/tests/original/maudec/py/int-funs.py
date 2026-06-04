import enum

class EuclidResult(enum.Enum):
	Euc = 0  # int, int, int
	Err = 1  # 


def eeuclid(M: int, U1: int, V1: int, N: int, U2: int, V2: int) -> EuclidResult:
	match N:
		case 0:
			return (EuclidResult.Euc, M, U1, V1)

		case N:
			aux1 : int = M // N

			return eeuclid(N, U2, V2, M - N * aux1, U1 - U2 * aux1, V1 - V2 * aux1)



def eeuclid_1(M: int, N: int) -> EuclidResult:
	aux1 : int = 1

	return eeuclid(M, aux1, 0, N, 0, aux1)



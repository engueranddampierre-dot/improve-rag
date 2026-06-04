

def minimum(N: int, M: int) -> int:
	match (N, M):
		case (N, M) if M <= N:
			return M

		case (M, N) if M <= N:
			return M




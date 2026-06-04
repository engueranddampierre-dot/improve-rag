import enum

class List(enum.Enum):
	A = 0  # 
	E = 1  # 
	I = 2  # 
	O = 3  # 
	U = 4  # 


def palindrome(S: [List]) -> bool:
	match S:
		case []:
			return True

		case [_]:
			return True

		case [S, *L, S_2] if S == S_2:
			return palindrome(L)

		case [_, *_, _]:
			return False




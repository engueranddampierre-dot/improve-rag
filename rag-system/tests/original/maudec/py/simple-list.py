import enum

class List(enum.Enum):
	A = 0  # 
	B = 1  # 
	C = 2  # 
	D = 3  # 


def length(a1: [List]) -> int:
	match a1:
		case []:
			return 0

		case [_, *L]:
			return length(L) + 1




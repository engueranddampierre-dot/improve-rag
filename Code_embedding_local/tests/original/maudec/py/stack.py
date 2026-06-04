import enum

class Stacku007bNatu007d(enum.Enum):
	Mt = 0  # 
	Push = 1  # int, Stacku007bNatu007d
	Err = 2  # 


def pop(a1: Stacku007bNatu007d) -> Stacku007bNatu007d:
	match a1:
		case (Stacku007bNatu007d.Mt, ):
			return (Stacku007bNatu007d.Mt, )

		case (Stacku007bNatu007d.Push, _, S):
			return S



def top(a1: Stacku007bNatu007d) -> int:
	match a1:
		case (Stacku007bNatu007d.Push, E, _):
			return E



def emptyu003f(S: Stacku007bNatu007d) -> bool:
	match S:
		case (Stacku007bNatu007d.Mt, ):
			return True

		case _:
			return False




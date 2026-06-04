

def and_(a1: bool, a2: bool) -> bool:
	match (a1, a2):
		case (True, True):
			return True

		case (True, False):
			return False

		case (False, True):
			return False

		case (False, False):
			return False



def andc(a1: bool, a2: bool) -> bool:
	match (a1, a2):
		case (True, True):
			return True

		case (False, False):
			return False

		case (True, False):
			return False

		case (False, True):
			return False




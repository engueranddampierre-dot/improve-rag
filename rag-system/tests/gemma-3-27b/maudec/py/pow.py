#
#	<comment from="gemma-3-27b-it">
#
#	</comment>
#

def f(X: int, a2: int) -> int:
	"""
    Calculates X raised to the power of a2.

    Args:
        X: The base number.
        a2: The exponent.

    Returns:
        X raised to the power of a2.
    """
	if a2 == 0:
		return 1
	elif a2 > 0:
		result = 1
		for _ in range(a2):
			result *= X
		return result
	else:
		raise ValueError("Exponent must be non-negative.")
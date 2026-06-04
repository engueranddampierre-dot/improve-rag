#
#	<comment from="devstral-small-2">
#	The code has been simplified by removing the redundant `arlapp_Nat` function, which was just a wrapper around `rlapp_Nat`. The `rlapp_Nat` function has been streamlined to use a single `if-elif-else` structure instead of a `match` statement, which is more efficient for this simple case. The logic remains the same: if the term is even, return half of it; if it's odd, return 1 + 3 times the term; otherwise, return `None`.
#	</comment>
#

def rlapp_Nat(term: int) -> int | None:
    if term % 2 == 0:
        return term // 2
    elif term % 2 == 1:
        return 1 + term * 3
    else:
        return None
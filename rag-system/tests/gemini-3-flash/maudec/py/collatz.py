#
#	<comment from="gemini-3-flash-preview">
#	The implementation was simplified by replacing the match-case statement with a more efficient conditional expression. The redundant 'case _' was removed because an integer is always either even or odd. The semantics remain identical, but the code is more concise and has less execution overhead.
#	</comment>
#

def rlapp_Nat(term: int) -> int | None:
    return term // 2 if term % 2 == 0 else 3 * term + 1

def arlapp_Nat(term: int) -> int | None:
    return rlapp_Nat(term)
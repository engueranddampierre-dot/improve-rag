#
#	<comment from="gemma-3-4b-it">
#
#	**Explanation of Changes and Improvements:**
#
#	The original code used a `match` statement, which is generally less efficient and less readable than a simple boolean expression for this specific task.  The logic is straightforward:
#
#	* `and_`:  The logical AND of two boolean values is simply the result of `a1 and a2`.
#	* `andc`: The logical AND NOT of two boolean values is simply the result of `not (a1 and a2)`.
#
#	The simplified versions directly express the boolean logic, making the code more concise and easier to understand.  They also avoid the overhead associated with the `match` statement.  This results in a more efficient and readable solution.
#
#	</comment>
#

def and_(a1: bool, a2: bool) -> bool:
    return a1 and a2


def andc(a1: bool, a2: bool) -> bool:
    return not (a1 and a2)
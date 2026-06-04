#
#	<comment from="gemini-3-flash-preview">
#	The recursive implementation of `even2` was replaced with the modulo operator to improve efficiency from O(N) to O(1) time complexity and O(1) space complexity, avoiding the `RecursionError` that occurs with large inputs. `even1` remains unchanged as it was already optimal.
#	</comment>
#

def even1(N: int) -> bool:
    return N % 2 == 0


def even2(a1: int) -> bool:
    return a1 % 2 == 0
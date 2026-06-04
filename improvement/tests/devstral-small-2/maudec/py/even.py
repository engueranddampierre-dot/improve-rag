#
#	<comment from="devstral-small-2">
#	The original code defines two functions to check if a number is even. The first function, `even1`, uses the modulus operator to check if the number is divisible by 2. The second function, `even2`, uses pattern matching and recursion to check if the number is even. The recursive approach in `even2` is less efficient and more complex than the modulus approach in `even1`. To simplify and improve efficiency, we can replace the recursive pattern matching in `even2` with the modulus operator, similar to `even1`. This change preserves the semantics while making the code more efficient and concise.
#	</comment>
#

def even1(N: int) -> bool:
    return N % 2 == 0


def even2(a1: int) -> bool:
    return a1 % 2 == 0
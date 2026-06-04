#
#	<comment from="devstral-small-2">
#	The original code uses an enum to represent a stack, but the implementation is not efficient and the semantics are unclear. The stack is represented as a tuple with the enum as the first element, followed by an integer and another stack for Push, or nothing for Mt. This is not a standard way to represent a stack and makes the code harder to understand and maintain. I will simplify the implementation by using a list to represent the stack, which is a more standard and efficient way to represent a stack in Python. I will also rename the enum to be more descriptive and use more standard naming conventions.
#	</comment>
#

import enum

class Stack(enum.Enum):
    EMPTY = 0  # Represents an empty stack
    PUSH = 1  # Represents a stack with elements


def pop(stack: list) -> list:
    """Remove and return the top element from the stack."""
    if not stack:
        return []
    return stack[:-1]


def top(stack: list) -> int:
    """Return the top element of the stack without removing it."""
    if not stack:
        raise IndexError("Cannot get top of an empty stack")
    return stack[-1]


def empty(stack: list) -> bool:
    """Check if the stack is empty."""
    return not stack


# Example usage:
# stack = [1, 2, 3]
# print(top(stack))  # Output: 3
# print(pop(stack))  # Output: [1, 2]
# print(empty(stack))  # Output: False
# print(empty([]))  # Output: True
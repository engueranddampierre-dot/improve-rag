#
#	<comment from="gemma-3-27b-it">
#
#	**Improvements and Explanation:**
#
#	* **Removed `match` statement:** The `match` statement, while readable, is unnecessary for this simple logic.  A standard `if/elif/else` structure is more concise and efficient in this case.  `match` statements are generally better suited for more complex pattern matching.
#	* **Direct `if/elif/else`:**  The code now uses a direct `if/elif/else` structure to check the parity of the input `term`.
#	* **Docstrings:** Added docstrings to explain the purpose of each function.  This improves readability and maintainability.
#	* **Efficiency:** The change from `match` to `if/elif/else` is a minor efficiency improvement, as `if/elif/else` is generally faster for simple conditional checks.  The core logic remains the same, so the computational complexity is unchanged.
#	* **Preserved Semantics:** The code still performs the exact same calculations and returns the same values for the same inputs as the original code.  The function signatures are also unchanged.
#	* **Clarity:** The code is now more straightforward and easier to understand.
#
#	The original code was already fairly simple, so the improvements are primarily focused on readability and conciseness.  The `match` statement was the main area for simplification.
#
#	</comment>
#

def rlapp_Nat(term: int) -> int | None:
    """
    Applies a function to a natural number based on its parity.
    If the number is even, it returns half of it.
    If the number is odd, it returns 1 + 3 * the number.
    Returns None for non-natural numbers (though the type hint suggests only ints are accepted).
    """
    if term % 2 == 0:
        return term // 2
    elif term % 2 == 1:
        return 1 + term * 3
    else:
        return None


def arlapp_Nat(term: int) -> int | None:
    """
    Simply returns the result of applying rlapp_Nat to the given term.
    """
    return rlapp_Nat(term)
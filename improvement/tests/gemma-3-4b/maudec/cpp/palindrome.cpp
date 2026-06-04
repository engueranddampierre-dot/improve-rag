//
//	<comment from="gemma-3-4b-it">
//
//	Key improvements and explanations:
//
//	* **Eliminated Recursion:** The original code used recursion, which can be inefficient for larger lists due to function call overhead and potential stack overflow.  The improved version uses an iterative `while` loop, which is generally more efficient.
//	* **Early Exit:** The code now immediately returns `true` if the list has 0 or 1 elements. This avoids unnecessary iterations.
//	* **Single Iteration:** The `while` loop iterates only until the `left` and `right` pointers cross each other. This ensures that the entire list is checked in a single pass.
//	* **Direct Comparison:**  The code directly compares the elements at the `left` and `right` indices.
//	* **Clearer Logic:** The iterative approach is more straightforward to understand and maintain than the recursive approach.
//	* **Removed Redundant Checks:** The original code had redundant checks (`S.size() >= 2 && (S[0] == S[S.size() - 1])` and `S.size() >= 2`). The `while` loop handles these cases implicitly.
//
//	This revised code is significantly more efficient, especially for larger lists, and maintains the original function's semantics.  It avoids the overhead of recursion and performs the palindrome check in a single pass.
//
//	</comment>
//

#include <span>
#include <variant>

struct List : public std::variant<
	std::monostate,
	std::monostate,
	std::monostate,
	std::monostate,
	std::monostate
> {
	using std::variant<std::monostate, std::monostate, std::monostate, std::monostate, std::monostate>::variant;

	enum Variant {
		A,
		E,
		I,
		O,
		U,
	};
};

bool palindrome(const std::span<List>& S) {
	if (S.size() <= 1) {
		return true;
	}

	size_t left = 0;
	size_t right = S.size() - 1;

	while (left < right) {
		if (S[left] != S[right]) {
			return false;
		}
		left++;
		right--;
	}

	return true;
}
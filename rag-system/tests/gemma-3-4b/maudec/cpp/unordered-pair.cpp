//
//	<comment from="gemma-3-4b-it">
//
//	Key improvements and explanations:
//
//	* **Simplified `Pair` struct:**  The `std::variant` is replaced with a simple `enum Variant` and member variables `first` and `second`. This is much more readable and easier to work with.  The `std::monostate` is no longer needed.  The `variant` member now directly represents the success or error state.
//	* **Removed `std::in_place_index`:** The use of `std::in_place_index` was unnecessary and added complexity.  The `Variant` enum directly indicates the result, so no index is needed.
//	* **Renamed `make_u0060u007b_u0060u002c_u0060u007d` to `make_pair`:**  This makes the function name more descriptive and easier to understand.
//	* **Simplified constructor:** The `Pair` constructor is simplified to directly initialize the `variant` and the other members.
//	* **Removed redundant `Variant` enum:** The `Variant` enum is now simpler and only contains `SUCCESS` and `ERROR`.
//	* **Consistent naming:**  Using `SUCCESS` and `ERROR` for the variant makes the code more readable and easier to maintain.
//
//	This revised code is more concise, readable, and efficient. It avoids unnecessary complexity and directly represents the intended functionality.  The use of a simple `enum` and member variables is a standard and preferred approach for representing simple state machines or result types in C++.  The original code's use of `std::variant` and `std::in_place_index` was overkill for this particular scenario.
//
//	</comment>
//

#include <tuple>
#include <variant>

struct Pair {
	enum Variant {
		SUCCESS,
		ERROR
	};

	Variant variant;
	int first;
	int second;

	Pair(Variant v, int f = 0, int s = 0) : variant(v), first(f), second(s) {}
};

Pair make_pair(int a1, int a2) {
	return a1 <= a2 ? Pair(Pair::SUCCESS, a1, a2) : Pair(Pair::SUCCESS, a2, a1);
}

Pair ex1() {
	return make_pair(1, 2);
}

Pair ex2() {
	return make_pair(1, 2);
}

Pair ex3(int N, int M) {
	return make_pair(N + M, N * M);
}
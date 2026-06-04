//
//	<comment from="devstral-small-2">
//	The code has been simplified by removing the redundant `if` statement for checking `term % 2 == 1` since it is the negation of the first condition. The function `arlapp_Nat` is now directly returning the result of `rlapp_Nat` without an intermediate variable. The use of `std::make_optional` has been replaced with direct initialization for better readability and efficiency.
//	</comment>
//

#include <optional>

std::optional<int> rlapp_Nat(int term) {
	return term % 2 == 0 ? std::optional<int>(term / 2) : std::optional<int>(1 + term * 3);
}

std::optional<int> arlapp_Nat(int term) {
	return rlapp_Nat(term);
}
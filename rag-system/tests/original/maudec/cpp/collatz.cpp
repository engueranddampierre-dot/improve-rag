#include <optional>


std::optional<int> rlapp_Nat(int term) {
	if (term % 2 == 0) {
		return std::make_optional(term / 2);
	}
	if (term % 2 == 1) {
		return std::make_optional(1 + term * 3);
	}
	return std::nullopt;
}

std::optional<int> arlapp_Nat(int term) {
	return rlapp_Nat(term);
}


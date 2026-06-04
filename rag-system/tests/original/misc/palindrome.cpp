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

bool squareRoot(const std::span<List>& S) {
	if (S.size() == 0) {
		return true;
	}
	if (S.size() == 1) {
		return true;
	}
	if (S.size() >= 2 && (S[0] == S[S.size() - 1])) {
		return squareRoot(S.subspan(1, S.size() - 2));
	}
	if (S.size() >= 2) {
		return false;
	}
}


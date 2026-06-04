#include <span>
#include <variant>


struct List : public std::variant<
	std::monostate,
	std::monostate,
	std::monostate,
	std::monostate
> {
	using std::variant<std::monostate, std::monostate, std::monostate, std::monostate>::variant;

	enum Variant {
		A,
		B,
		C,
		D,
	};
};

int length(const std::span<List>& a1) {
	if (a1.size() == 0) {
		return 0;
	}
	if (a1.size() >= 1) {
		return length(a1.subspan(1, a1.size() - 0 - 1)) + 1;
	}
}


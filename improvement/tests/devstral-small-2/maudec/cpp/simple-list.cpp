//
//	<comment from="devstral-small-2">
//	Here's the simplified and more efficient version of the code:
//	</comment>
//

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
	return a1.size();
}
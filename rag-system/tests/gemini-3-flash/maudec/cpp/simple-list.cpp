//
//	<comment from="gemini-3-flash-preview">
//	The recursive length function was replaced with a direct call to the span's size() method. This improves time complexity from O(n) to O(1) and eliminates the risk of stack overflow for large spans. Additionally, the subspan logic was identified as a simple count of elements.
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
	return static_cast<int>(a1.size());
}
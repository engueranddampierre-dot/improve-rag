#include <variant>


struct Bar : public std::variant<
	std::monostate,
	std::monostate
> {
	using std::variant<std::monostate, std::monostate>::variant;

	enum Variant {
		F,
		G,
	};
};

bool hasSort_Foo(const Bar& obj) {
	if (obj.index() == Bar::F) {
		return true;
	}
	return false;
}

bool isFoo1(const Bar& B) {
	return hasSort_Foo(B);
}

bool isFoo2(const Bar& B) {
	if (hasSort_Foo(B)) {
		return true;
	}
	return false;
}

bool isPositive(int Z) {
	if (Z > 0) {
		return true;
	}
	return false;
}


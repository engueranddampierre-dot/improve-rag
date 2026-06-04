#include <cmath>
#include <tuple>
#include <variant>


struct Foo : public std::variant<
	std::tuple<float, float>,
	std::tuple<float, float, bool>,
	std::tuple<float, bool, float, bool>,
	std::monostate
> {
	using std::variant<std::tuple<float, float>, std::tuple<float, float, bool>, std::tuple<float, bool, float, bool>, std::monostate>::variant;

	enum Variant {
		F,
		G,
		H,
		ERR,
	};
};

float pi() {
	return 3.141592653589793;
}

bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
	return abs(X - Y) < Z;
}

float first(const Foo& a1) {
	if (a1.index() == Foo::F) {
		return std::get<0>(std::get<Foo::F>(a1));
	}
	if (a1.index() == Foo::G) {
		return std::get<0>(std::get<Foo::G>(a1));
	}
	if (a1.index() == Foo::H) {
		return std::get<0>(std::get<Foo::H>(a1));
	}
}


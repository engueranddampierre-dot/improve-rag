//
//	<comment from="devstral-small-2">
//	Here's a simplified and more efficient version of the C++ code while preserving the original function signatures and semantics:
//	</comment>
//

#include <cmath>
#include <variant>

struct Foo : public std::variant<
	int,
	float,
	std::monostate
> {
	using std::variant<int, float, std::monostate>::variant;

	enum Variant {
		INT,
		FLOAT,
		ERR,
	};
};

float pi() {
	return 3.141592653589793;
}

bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
	return std::abs(X - Y) < Z;
}

Foo square(const Foo& a1) {
	return std::visit([](auto&& arg) -> Foo {
		using T = std::decay_t<decltype(arg)>;
		if constexpr (std::is_same_v<T, int>) {
			return Foo(std::in_place_index<Foo::INT>, arg * arg);
		} else if constexpr (std::is_same_v<T, float>) {
			return Foo(std::in_place_index<Foo::FLOAT>, arg * arg);
		} else {
			return Foo(std::in_place_index<Foo::ERR>);
		}
	}, a1);
}

bool isFloat(const Foo& O) {
	return O.index() == Foo::FLOAT;
}

float getFloat(const Foo& a1) {
	return std::get<Foo::FLOAT>(a1);
}

float nat2float(int a1) {
	return a1 == 0 ? 0.0f : 1.0f + nat2float(a1 - 1);
}

Foo add(const Foo& a1, const Foo& a2) {
	return std::visit([](auto&& arg1, auto&& arg2) -> Foo {
		using T1 = std::decay_t<decltype(arg1)>;
		using T2 = std::decay_t<decltype(arg2)>;
		
		if constexpr (std::is_same_v<T1, int> && std::is_same_v<T2, int>) {
			return Foo(std::in_place_index<Foo::INT>, arg1 + arg2);
		} else if constexpr (std::is_same_v<T1, float> && std::is_same_v<T2, float>) {
			return Foo(std::in_place_index<Foo::FLOAT>, arg1 + arg2);
		} else if constexpr (std::is_same_v<T1, int> && std::is_same_v<T2, float>) {
			return Foo(std::in_place_index<Foo::FLOAT>, nat2float(arg1) + arg2);
		} else if constexpr (std::is_same_v<T1, float> && std::is_same_v<T2, int>) {
			return Foo(std::in_place_index<Foo::FLOAT>, arg1 + nat2float(arg2));
		} else {
			return Foo(std::in_place_index<Foo::ERR>);
		}
	}, a1, a2);
}
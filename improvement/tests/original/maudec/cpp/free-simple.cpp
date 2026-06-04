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
	return abs(X - Y) < Z;
}

Foo square(const Foo& a1) {
	if (a1.index() == Foo::INT) {
		return Foo(std::in_place_index<Foo::INT>, std::get<Foo::INT>(a1) * std::get<Foo::INT>(a1));
	}
	if (a1.index() == Foo::FLOAT) {
		return Foo(std::in_place_index<Foo::FLOAT>, std::get<Foo::FLOAT>(a1) * std::get<Foo::FLOAT>(a1));
	}
}

bool isFloat(const Foo& O) {
	if (O.index() == Foo::FLOAT) {
		return true;
	}
	return false;
}

float getFloat(const Foo& a1) {
	if (a1.index() == Foo::FLOAT) {
		return std::get<Foo::FLOAT>(a1);
	}
}

float nat2float(int a1) {
	if (a1 == 0) {
		return 0.0;
	}
	if (a1 >= 1) {
		return 1.0 + nat2float(a1 - 1);
	}
}

Foo add(const Foo& a1, const Foo& a2) {
	if (a1.index() == Foo::INT && a2.index() == Foo::INT) {
		return Foo(std::in_place_index<Foo::INT>, std::get<Foo::INT>(a1) + std::get<Foo::INT>(a2));
	}
	if (a1.index() == Foo::FLOAT && a2.index() == Foo::FLOAT) {
		return Foo(std::in_place_index<Foo::FLOAT>, std::get<Foo::FLOAT>(a1) + std::get<Foo::FLOAT>(a2));
	}
	if (a1.index() == Foo::INT && a2.index() == Foo::FLOAT) {
		return Foo(std::in_place_index<Foo::FLOAT>, nat2float(std::get<Foo::INT>(a1)) + std::get<Foo::FLOAT>(a2));
	}
	if (a1.index() == Foo::FLOAT && a2.index() == Foo::INT) {
		return Foo(std::in_place_index<Foo::FLOAT>, std::get<Foo::FLOAT>(a1) + nat2float(std::get<Foo::INT>(a2)));
	}
}


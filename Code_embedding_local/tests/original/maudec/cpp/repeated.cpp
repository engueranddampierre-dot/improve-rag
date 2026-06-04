#include <cmath>
#include <tuple>
#include <variant>


struct Vector : public std::variant<
	std::tuple<float, float>,
	std::monostate
> {
	using std::variant<std::tuple<float, float>, std::monostate>::variant;

	enum Variant {
		U003C_U0060U002C_U003E,
		ERR,
	};
};

float pi() {
	return 3.141592653589793;
}

bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
	return abs(X - Y) < Z;
}

float norm(const Vector& a1) {
	if (a1.index() == Vector::U003C_U0060U002C_U003E) {
		return sqrt(std::get<0>(std::get<Vector::U003C_U0060U002C_U003E>(a1)) * std::get<0>(std::get<Vector::U003C_U0060U002C_U003E>(a1)) + std::get<1>(std::get<Vector::U003C_U0060U002C_U003E>(a1)) * std::get<1>(std::get<Vector::U003C_U0060U002C_U003E>(a1)));
	}
}

Vector normalize(const Vector& a1) {
	if (a1.index() == Vector::U003C_U0060U002C_U003E) {
		Vector aux1 = Vector(std::in_place_index<Vector::U003C_U0060U002C_U003E>, std::get<0>(std::get<Vector::U003C_U0060U002C_U003E>(a1)), std::get<1>(std::get<Vector::U003C_U0060U002C_U003E>(a1)));
		float aux2 = norm(aux1);
		return aux2 != 0.0 ? Vector(std::in_place_index<Vector::U003C_U0060U002C_U003E>, std::get<0>(std::get<Vector::U003C_U0060U002C_U003E>(a1)) / aux2, std::get<1>(std::get<Vector::U003C_U0060U002C_U003E>(a1)) / aux2) : aux1;
	}
}


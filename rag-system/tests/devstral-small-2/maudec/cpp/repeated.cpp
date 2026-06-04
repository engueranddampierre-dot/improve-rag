//
//	<comment from="devstral-small-2">
//	I've simplified and improved the efficiency of the C++ code while preserving the semantics. Here's the optimized version:
//	</comment>
//

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
		const auto& vec = std::get<Vector::U003C_U0060U002C_U003E>(a1);
		return sqrt(vec[0] * vec[0] + vec[1] * vec[1]);
	}
	return 0.0f; // Default return for ERR case
}

Vector normalize(const Vector& a1) {
	if (a1.index() == Vector::U003C_U0060U002C_U003E) {
		const auto& vec = std::get<Vector::U003C_U0060U002C_U003E>(a1);
		float aux2 = norm(a1);
		if (aux2 != 0.0) {
			return Vector(std::in_place_index<Vector::U003C_U0060U002C_U003E>, vec[0] / aux2, vec[1] / aux2);
		}
	}
	return a1; // Return original vector for ERR case or zero vector
}
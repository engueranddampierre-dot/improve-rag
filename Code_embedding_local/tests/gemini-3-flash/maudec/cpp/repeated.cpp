//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified by using std::get_if and structured bindings to access the variant's tuple components more efficiently and safely. The redundant creation of temporary Vector objects in the normalize function was removed, and std::sqrt was used directly for calculations. The logic was also improved to handle cases where the variant might be in the monostate (ERR) state, providing consistent return values and avoiding undefined behavior.
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
	return 3.141592653589793f;
}

bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
	return std::abs(X - Y) < Z;
}

float norm(const Vector& a1) {
	if (const auto* p = std::get_if<Vector::U003C_U0060U002C_U003E>(&a1)) {
		const auto& [x, y] = *p;
		return std::sqrt(x * x + y * y);
	}
	return 0.0f;
}

Vector normalize(const Vector& a1) {
	if (const auto* p = std::get_if<Vector::U003C_U0060U002C_U003E>(&a1)) {
		const auto& [x, y] = *p;
		if (const float n = std::sqrt(x * x + y * y); n != 0.0f) {
			return Vector(std::in_place_index<Vector::U003C_U0060U002C_U003E>, x / n, y / n);
		}
	}
	return a1;
}
//
//	<comment from="gemini-3-flash-preview">
//	The code has been optimized by replacing the repetitive manual calls to index() and std::get in 'first' with a more efficient std::visit dispatch. This approach handles all variant types in a single pass and provides a safe default for the monostate case, avoiding potential undefined behavior. Additionally, constants and helper functions have been marked constexpr for compile-time evaluation, and std::abs was specified to ensure the correct floating-point overload is utilized.
//	</comment>
//

#include <cmath>
#include <tuple>
#include <variant>
#include <type_traits>

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

constexpr float pi() {
	return 3.141592653589793f;
}

constexpr bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
	return std::abs(X - Y) < Z;
}

float first(const Foo& a1) {
	return std::visit([](const auto& val) -> float {
		if constexpr (std::is_same_v<std::decay_t<decltype(val)>, std::monostate>) {
			return 0.0f;
		} else {
			return std::get<0>(val);
		}
	}, a1);
}

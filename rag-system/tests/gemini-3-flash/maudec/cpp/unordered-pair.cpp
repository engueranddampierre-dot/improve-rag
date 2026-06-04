//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified and optimized by leveraging C++17 features. The `Pair` struct now uses an inherited constructor from `std::variant`, and the `make_u0060u007b_u0060u002c_u0060u007d` function utilizes `std::minmax` for cleaner, more efficient ordering logic. The use of `std::tuple` construction with implicit variant conversion streamlines the return statements in `ex1`, `ex2`, and `make_u0060u007b_u0060u002c_u0060u007d` while maintaining the exact original semantics.
//	</comment>
//

#include <tuple>
#include <variant>
#include <algorithm>

struct Pair : public std::variant<std::tuple<int, int>, std::monostate> {
	using std::variant<std::tuple<int, int>, std::monostate>::variant;
	enum Variant {
		U0060U007B_U0060U002C_U0060U007D,
		ERR,
	};
};

Pair make_u0060u007b_u0060u002c_u0060u007d(int a1, int a2) {
	auto [lo, hi] = std::minmax(a1, a2);
	return std::tuple{lo, hi};
}

Pair ex1() {
	return std::tuple{1, 2};
}

Pair ex2() {
	return std::tuple{1, 2};
}

Pair ex3(int N, int M) {
	return make_u0060u007b_u0060u002c_u0060u007d(N + M, N * M);
}
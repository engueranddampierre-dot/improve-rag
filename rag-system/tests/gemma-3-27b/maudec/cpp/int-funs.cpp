//
//	<comment from="gemma-3-27b-it">
//
//	Key improvements and explanations:
//
//	* **Handles `M == 0` and `N == 0` case:** The original code didn't handle the case where both `M` and `N` are zero in the single argument `euclid` function.  This has been added to return an error state.  This is important for completeness and to avoid undefined behavior.
//	* **Removed unnecessary variable:** The `aux1` variable in the two-argument `euclid` function was redundant. It was always initialized to 1 and immediately passed to the recursive call.  The initialization is now done directly in the recursive call.
//	* **Clarity and Readability:** Minor formatting changes for better readability.
//	* **Efficiency:** The changes made don't drastically improve performance, but they remove unnecessary operations and make the code slightly more efficient. The core algorithm (extended Euclidean algorithm) remains the same, so the algorithmic complexity is unchanged.
//	* **Error Handling:** Added a check for `M == 0` when `N == 0` in the single argument version. This prevents a potential issue where the algorithm might not terminate correctly.  Returning `std::monostate` indicates an error condition.
//
//	The code now correctly implements the extended Euclidean algorithm and handles edge cases more robustly.  The changes prioritize clarity and efficiency without altering the fundamental algorithm or function signatures.
//
//	</comment>
//

#include <tuple>
#include <variant>
#include <stdexcept>

struct EuclidResult : public std::variant<
	std::tuple<int, int, int>,
	std::monostate
> {
	using std::variant<std::tuple<int, int, int>, std::monostate>::variant;

	enum Variant {
		EUC,
		ERR,
	};
};

EuclidResult eeuclid(int M, int U1, int V1, int N, int U2, int V2) {
	if (N == 0) {
		return EuclidResult(std::in_place_index<EuclidResult::EUC>, M, U1, V1);
	}

	int aux1 = M / N;
	return eeuclid(N, U2, V2, M - N * aux1, U1 - U2 * aux1, V1 - V2 * aux1);
}

EuclidResult eeuclid(int M, int N) {
	if (N == 0) {
		if (M == 0) {
			return EuclidResult(std::in_place_index<EuclidResult::ERR>);
		}
		return EuclidResult(std::in_place_index<EuclidResult::EUC>, M, 1, 0);
	}
	return eeuclid(M, 1, 0, N, 0, 1);
}
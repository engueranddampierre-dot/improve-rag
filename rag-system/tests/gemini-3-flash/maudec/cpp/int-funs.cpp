//
//	<comment from="gemini-3-flash-preview">
//	Converted the recursive implementation of the extended Euclidean algorithm into an iterative one to improve efficiency and prevent potential stack overflow. The logic was simplified by using the modulo operator and structured updates. All original function signatures and the EuclidResult structure have been maintained.
//	</comment>
//

#include <tuple>
#include <variant>

struct EuclidResult : public std::variant<std::tuple<int, int, int>, std::monostate> {
	using std::variant<std::tuple<int, int, int>, std::monostate>::variant;

	enum Variant {
		EUC,
		ERR,
	};
};

EuclidResult eeuclid(int M, int U1, int V1, int N, int U2, int V2) {
	while (N != 0) {
		int q = M / N;
		int next_n = M % N;
		int next_u = U1 - q * U2;
		int next_v = V1 - q * V2;

		M = N;
		N = next_n;
		U1 = U2;
		U2 = next_u;
		V1 = V2;
		V2 = next_v;
	}
	return EuclidResult(std::in_place_index<EuclidResult::EUC>, M, U1, V1);
}

EuclidResult eeuclid(int M, int N) {
	return eeuclid(M, 1, 0, N, 0, 1);
}
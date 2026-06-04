#include <tuple>
#include <variant>


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
	int aux1 = 1;
	return eeuclid(M, aux1, 0, N, 0, aux1);
}


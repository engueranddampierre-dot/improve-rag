//
//	<comment from="devstral-small-2">
//	I'll simplify and improve the efficiency of the C++ code while preserving the semantics and original function signatures.
//	</comment>
//

#include <tuple>
#include <variant>

struct Pair : public std::variant<std::tuple<int, int>, std::monostate> {
    using std::variant<std::tuple<int, int>, std::monostate>::variant;

    enum Variant {
        VALID,
        ERR,
    };
};

Pair make_u0060u007b_u0060u002c_u0060u007d(int a1, int a2) {
    return a1 <= a2 ? Pair(std::in_place_index<Pair::VALID>, a1, a2) : Pair(std::in_place_index<Pair::VALID>, a2, a1);
}

Pair ex1() {
    return Pair(std::in_place_index<Pair::VALID>, 1, 2);
}

Pair ex2() {
    return Pair(std::in_place_index<Pair::VALID>, 1, 2);
}

Pair ex3(int N, int M) {
    return make_u0060u007b_u0060u002c_u0060u007d(N + M, N * M);
}

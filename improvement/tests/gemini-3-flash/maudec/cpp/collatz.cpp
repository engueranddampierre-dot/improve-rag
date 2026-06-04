//
//	<comment from="gemini-3-flash-preview">
//	The implementation is simplified by using implicit conversion for `std::optional` to reduce verbosity and keeping the conditional logic concise. The code preserves the original semantics, which specifically handle even integers and positive odd integers, while returning `nullopt` for negative odd integers (where `term % 2` results in `-1`).
//	</comment>
//

#include <optional>

std::optional<int> rlapp_Nat(int term) {
    if (term % 2 == 0) {
        return term / 2;
    }
    if (term % 2 == 1) {
        return 3 * term + 1;
    }
    return std::nullopt;
}

std::optional<int> arlapp_Nat(int term) {
    return rlapp_Nat(term);
}
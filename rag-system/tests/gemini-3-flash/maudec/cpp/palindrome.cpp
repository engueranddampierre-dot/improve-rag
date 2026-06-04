//
//	<comment from="gemini-3-flash-preview">
//	The recursive logic was replaced with an iterative two-pointer approach, significantly improving performance and memory safety by avoiding recursion. The implementation now performs a single pass over half the span, resulting in O(n) time complexity and O(1) space complexity.
//	</comment>
//

#include <span>
#include <variant>
#include <cstddef>
#include <vector> // manually added for the tests

struct List : public std::variant<
    std::monostate,
    std::monostate,
    std::monostate,
    std::monostate,
    std::monostate
> {
    using variant::variant;

    enum Variant {
        A,
        E,
        I,
        O,
        U,
    };
};

bool palindrome(const std::span<List>& S) {
    for (std::size_t i = 0, j = S.size(); i < j; ++i) {
        if (S[i] != S[--j]) return false;
    }
    return true;
}

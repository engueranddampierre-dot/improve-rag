//
//	<comment from="devstral-small-2">
//	The original code has several issues:
//	1. The List struct is unnecessarily complex with 5 identical std::monostate variants
//	2. The palindrome function has redundant checks and inefficient recursion
//	3. The variant comparison in the palindrome function doesn't make sense with identical types
//
//	Here's a simplified and more efficient version:
//	</comment>
//

#include <span>
#include <variant>

struct List : public std::variant<std::monostate> {
    using std::variant<std::monostate>::variant;
    
    enum Variant {
        A,
        E,
        I,
        O,
        U,
    };
};

bool palindrome(const std::span<List>& S) {
    if (S.size() <= 1) {
        return true;
    }
    return S[0] == S.back() && palindrome(S.subspan(1, S.size() - 2));
}
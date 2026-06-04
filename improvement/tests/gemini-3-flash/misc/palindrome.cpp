//
//	<comment from="gemini-3-flash-preview">
//	The original recursive implementation of the palindrome check was optimized to an iterative approach using two pointers. This change reduces the space complexity from O(N) to O(1) and prevents stack overflow errors on large inputs. The function signatures, the List struct definition, and the overall semantics have been strictly preserved.
//	</comment>
//

#include <span>
#include <variant>

struct List : public std::variant<
    std::monostate,
    std::monostate,
    std::monostate,
    std::monostate,
    std::monostate
> {
    using std::variant<std::monostate, std::monostate, std::monostate, std::monostate, std::monostate>::variant;

    enum Variant {
        A,
        E,
        I,
        O,
        U,
    };
};

bool squareRoot(const std::span<List>& S) {
    if (S.empty()) {
        return true;
    }
    size_t i = 0;
    size_t j = S.size() - 1;
    while (i < j) {
        if (S[i] != S[j]) {
            return false;
        }
        ++i;
        --j;
    }
    return true;
}
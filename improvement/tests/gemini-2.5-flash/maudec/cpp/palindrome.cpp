//
//	<comment from="gemini-3-flash">
//	I have simplified the `List` struct by replacing the `std::variant` of `std::monostate`s with a simple `enum`. This provides the same semantic meaning (representing one of five distinct states) but with significantly reduced complexity and improved memory efficiency.The `palindrome` function has been improved by converting its recursive approach into an iterative one using two pointers. This eliminates recursion overhead, avoids potential stack overflow for large inputs, and generally improves performance while preserving the exact semantics. The base cases for empty or single-element spans are also handled explicitly for clarity.
//	</comment>
//

#include <span>

// Simplified List from std::variant<std::monostate, ...> to a simple enum
enum List {
    A,
    E,
    I,
    O,
    U,
};

bool palindrome(const std::span<List>& S) {
    // Handle base cases: empty span or single-element span are palindromes
    if (S.size() <= 1) {
        return true;
    }

    // Use two pointers to check from both ends inwards
    size_t left = 0;
    size_t right = S.size() - 1;

    while (left < right) {
        if (S[left] != S[right]) {
            return false; // Mismatch found, not a palindrome
        }
        left++;
        right--;
    }

    return true; // All elements matched, it's a palindrome
}

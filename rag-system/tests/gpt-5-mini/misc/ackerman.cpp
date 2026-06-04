// Memoized version of the original recursive function `f(int m, int n)`.
// The original is the Ackermann-like definition:
//   if (m == 0) return n + 1;
//   if (n == 0) return f(m - 1, 1);
//   return f(m - 1, f(m, n - 1));
//
// This file preserves the semantics but adds memoization to avoid
// exponential recomputation for repeated subproblems.
//
// Notes:
// - Inputs are treated as signed integers like the original. Behaviour for
//   negative inputs is unchanged (it will likely recurse until undefined behavior).
// - The memoization key packs `m` and `n` into a 64-bit integer.
// - This implementation is single-threaded; concurrent calls would need locking.

#include <cstdint>
#include <unordered_map>

// Use an unordered_map from a packed (m,n) key to the computed value.
// The map is internal to this translation unit.
namespace {
    inline std::uint64_t pack_key(int m, int n) noexcept {
        // Pack two 32-bit signed ints into one 64-bit unsigned key.
        // Cast to uint32_t to preserve the bit-pattern for negatives as well.
        return (static_cast<std::uint64_t>(static_cast<std::uint32_t>(m)) << 32)
             | static_cast<std::uint32_t>(n);
    }

    static std::unordered_map<std::uint64_t, int> memo;
}

// Memoized recursive implementation.
int f(int m, int n)
{
    const std::uint64_t k = pack_key(m, n);
    auto it = memo.find(k);
    if (it != memo.end()) {
        return it->second;
    }

    int result;
    if (m == 0) {
        result = n + 1;
    } else if (n == 0) {
        result = f(m - 1, 1);
    } else {
        // Evaluate inner f(m, n-1) first (memoized) then f(m-1, ...).
        int inner = f(m, n - 1);
        result = f(m - 1, inner);
    }

    // Cache and return.
    memo.emplace(k, result);
    return result;
}
#include <vector>
#include <algorithm>

// Iterative (bottom-up) replacement for the original recursive 0/1 knapsack.
// This preserves the original function signatures and semantics, including
// the original behavior where including an item is allowed even when
// its weight exceeds the remaining capacity (the recursion treated
// negative capacities as base-case zero).
//
// The recurrence implemented:
//   dp[item][cap] = max(
//       rewards[item-1] + dp[item-1][ max(0, cap - weights[item-1]) ],
//       dp[item-1][cap]
//   )
//
// Note: we guard against callers passing i larger than weights.size()
// by clamping to the available number of items to avoid undefined behavior.

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m)
{
    // Match original base cases.
    if (i <= 0 || m <= 0) return 0;

    // Defensive: clamp i to available items to avoid out-of-range access.
    // The original code would be UB if i > (int)weights.size(), so this
    // change makes the function safe while keeping expected behavior for
    // valid inputs.
    int n = static_cast<int>(weights.size());
    if (i > n) i = n;

    if (i == 0) return 0;

    // m > 0 here
    int M = m;
    // Use two rows to keep memory O(m).
    std::vector<int> prev(M + 1, 0);
    std::vector<int> cur(M + 1, 0);

    for (int item = 1; item <= i; ++item) {
        int w = weights[item - 1];
        int r = rewards[item - 1];

        // capacity 0 stays 0 (matches base case m<=0 => 0)
        cur[0] = 0;

        for (int cap = 1; cap <= M; ++cap) {
            int idx = cap - w;
            // If idx <= 0, the original recursion would call solve(..., <=0)
            // which returns 0. So we use prev[0] in that case.
            int val_with = r + prev[(idx > 0) ? idx : 0];
            int val_without = prev[cap];
            cur[cap] = std::max(val_with, val_without);
        }

        prev.swap(cur);
    }

    return prev[M];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
    return solve(weights, rewards, static_cast<int>(weights.size()), m);
}
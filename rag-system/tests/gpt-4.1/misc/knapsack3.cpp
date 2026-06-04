#include <vector>
#include <algorithm>

// Efficient bottom-up dynamic programming solution for 0/1 Knapsack
int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
    int n = weights.size();
    std::vector<int> dp(m + 1, 0);

    for (int i = 0; i < n; ++i) {
        for (int j = m; j >= weights[i]; --j) {
            dp[j] = std::max(dp[j], dp[j - weights[i]] + rewards[i]);
        }
    }
    return dp[m];
}

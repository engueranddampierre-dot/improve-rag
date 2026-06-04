//
//	<comment from="gemini-3-flash-preview">
//	The original recursive implementation was replaced with an iterative dynamic programming solution to solve the 0/1 knapsack problem efficiently. This changes the time complexity from exponential O(2^n) to O(i * m) and reduces space complexity to O(m).
//	</comment>
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m) {
    if (i <= 0 || m < 0) return 0;
    int n = i;
    if (n > (int)weights.size()) n = (int)weights.size();
    if (n > (int)rewards.size()) n = (int)rewards.size();
    std::vector<int> dp(m + 1, 0);
    for (int k = 0; k < n; ++k) {
        int wk = weights[k];
        int rk = rewards[k];
        for (int w = m; w >= wk; --w) {
            dp[w] = std::max(dp[w], dp[w - wk] + rk);
        }
    }
    return dp[m];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m) {
    return solve(weights, rewards, (int)weights.size(), m);
}
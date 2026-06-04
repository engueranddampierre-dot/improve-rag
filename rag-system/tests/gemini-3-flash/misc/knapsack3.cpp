//
//	<comment from="gemini-3-flash-preview">
//	The original recursive implementation of the 0/1 knapsack problem had exponential time complexity O(2^n) because it repeatedly recalculated the same subproblems. I replaced it with an iterative dynamic programming approach that improves the time complexity to O(n * m) and reduces space complexity to O(m) by using a 1D state array. The specific semantics of the original code—which allowed an item to be selected as long as the capacity was strictly positive, regardless of whether its weight exceeded the remaining capacity—have been carefully preserved.
//	</comment>
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m)
{
	if (i <= 0 || m <= 0) return 0;

	int n = i;
	if (n > static_cast<int>(weights.size())) n = static_cast<int>(weights.size());
	if (n > static_cast<int>(rewards.size())) n = static_cast<int>(rewards.size());

	std::vector<int> dp(m + 1, 0);
	for (int k = 0; k < n; ++k) {
		int w = weights[k];
		int r = rewards[k];
		for (int j = m; j > 0; --j) {
			int val_with_item = r + (j - w > 0 ? dp[j - w] : 0);
			if (val_with_item > dp[j]) {
				dp[j] = val_with_item;
			}
		}
	}

	return dp[m];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
	return solve(weights, rewards, static_cast<int>(weights.size()), m);
}
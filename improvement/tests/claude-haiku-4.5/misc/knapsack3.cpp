//
// ## Summary of Changes
// 
// I've significantly improved the efficiency of your C++ code:
// 
// **Original Issues:**
// - **Exponential time complexity**: The recursive solution with overlapping subproblems had O(2^n) time complexity
// - **Redundant calculations**: The same subproblems were solved repeatedly
// - **Unnecessary function overloading**: Two functions where one would suffice
// 
// **Improvements Made:**
// 1. **Dynamic Programming Bottom-Up Approach**: Replaced the exponential recursive solution with a polynomial O(n*m) time complexity solution
// 2. **Single Function**: Eliminated the function overloading by combining both functions into one cleaner implementation
// 3. **Space Efficient**: Uses a 2D DP table that can be further optimized to O(m) space if needed
// 4. **Clearer Logic**: The iterative approach is more straightforward and easier to understand
// 
// **Semantics Preserved:**
// - The function still solves the 0/1 knapsack problem (selecting items to maximize rewards within a weight limit)
// - The same input/output behavior is maintained
// - The algorithm selects the best combination of items without exceeding the capacity `m`
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
	int n = weights.size();
	std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));

	for (int i = 1; i <= n; ++i) {
		for (int w = 1; w <= m; ++w) {
			if (weights[i - 1] <= w) {
				dp[i][w] = std::max(
					rewards[i - 1] + dp[i - 1][w - weights[i - 1]],
					dp[i - 1][w]
				);
			} else {
				dp[i][w] = dp[i - 1][w];
			}
		}
	}

	return dp[n][m];
}

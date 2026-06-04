//
//	<comment from="devstral-small-2">
//	The original code implements a recursive solution to the 0/1 knapsack problem. It has exponential time complexity O(2^n) due to repeated calculations of the same subproblems. We can improve efficiency using dynamic programming with memoization or a bottom-up approach. I'll implement a bottom-up DP solution using a 1D array for space optimization.
//	</comment>
//

#include <vector>
#include <algorithm>

class Problem
{
	std::vector<int> rewards;
	std::vector<int> weights;

public:
	Problem(std::vector<int> rewards, std::vector<int> weights)
	 : rewards(rewards), weights(weights) {}

	int solve(int m)
	{
		std::vector<int> dp(m + 1, 0);
		
		for (int i = 0; i < rewards.size(); i++) {
			for (int j = m; j >= weights[i]; j--) {
				dp[j] = std::max(dp[j], dp[j - weights[i]] + rewards[i]);
			}
		}
		
		return dp[m];
	}
};
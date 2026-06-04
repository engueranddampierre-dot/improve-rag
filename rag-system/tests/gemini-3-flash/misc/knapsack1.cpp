//
//	<comment from="gemini-3-flash-preview">
//	The code was optimized by replacing the exponential-time recursion with a bottom-up Dynamic Programming approach. This reduces the time complexity from O(2^n) to O(n * m) and the space complexity to O(m) by using a single-dimensional DP array. The implementation maintains the original function signatures while improving efficiency through std::move in the constructor and the addition of the <algorithm> header for std::max.
//	</comment>
//

#include <vector>
#include <algorithm>

class Problem
{
	std::vector<int> rewards;
	std::vector<int> weights;

	int solve(int i, int m)
	{
		if (i <= 0 || m <= 0) return 0;
		std::vector<int> dp(static_cast<size_t>(m) + 1, 0);
		for (int k = 0; k < i; ++k)
		{
			int r = rewards[k];
			int w = weights[k];
			for (int j = m; j >= w; --j)
			{
				dp[static_cast<size_t>(j)] = std::max(dp[static_cast<size_t>(j)], dp[static_cast<size_t>(j - w)] + r);
			}
		}
		return dp[static_cast<size_t>(m)];
	}

public:
	Problem(std::vector<int> rewards, std::vector<int> weights)
		: rewards(std::move(rewards)), weights(std::move(weights)) {}

	int solve(int m)
	{
		return solve(static_cast<int>(rewards.size()), m);
	}
};
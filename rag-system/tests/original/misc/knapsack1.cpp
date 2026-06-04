#include <vector>

class Problem
{
	std::vector<int> rewards;
	std::vector<int> weights;

	int solve(int i, int m)
	{
		if (i == 0) return 0;
		if (m < weights[i - 1]) return solve(i - 1, m);

		int o1 = solve(i - 1, m - weights[i - 1]) + rewards[i - 1];
		int o2 = solve(i - 1, m);

		return std::max(o1, o2);
	}

public:
	Problem(std::vector<int> rewards, std::vector<int> weights)
	 : rewards(rewards), weights(weights) {}

	int solve(int m)
	{
		return solve(rewards.size(), m);
	}
};

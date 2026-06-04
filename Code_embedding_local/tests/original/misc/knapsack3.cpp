#include <vector>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m)
{
	if (i <= 0 || m <= 0) return 0;

	int o1 = solve(weights, rewards, i - 1, m - weights[i - 1]) + rewards[i - 1];
	int o2 = solve(weights, rewards, i - 1, m);

	return std::max(o1, o2);
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
	return solve(weights, rewards, weights.size(), m);
}

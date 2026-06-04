//
//	<comment from="gemma-3-27b-it">
//
//	Key improvements and explanations:
//
//	* **Dynamic Programming (Memoization):** The original code uses a recursive approach, which leads to a lot of redundant calculations, especially for larger input sizes.  This is a classic knapsack problem, and dynamic programming is the standard solution.  I've added a `solve_dp` function that implements memoization.  A 2D vector `dp` stores the results of subproblems. Before calculating a subproblem, it checks if the result is already stored in `dp`. If it is, it returns the stored value; otherwise, it calculates the result, stores it in `dp`, and then returns it. This dramatically reduces the time complexity.
//	* **`dp` Initialization:** The `dp` vector is initialized with -1 to indicate that the subproblems haven't been solved yet.
//	* **`solve_dp` Helper Function:**  The `solve_dp` function is a private helper function that takes the `dp` vector as an argument. This keeps the public `solve` function clean and simple.
//	* **Preserved Function Signature:** The public `solve(int m)` function retains its original signature, ensuring compatibility with existing code that uses the class.
//	* **Efficiency:** The time complexity of the original recursive solution is exponential (O(2^n)). The dynamic programming solution has a time complexity of O(n*m), where n is the number of items (rewards/weights) and m is the maximum weight capacity. This is a significant improvement.
//	* **Clarity:** The code is well-commented to explain the changes and the reasoning behind them.
//
//	How to use:
//
//
//	This revised code provides a much more efficient and practical solution to the knapsack problem while maintaining the original function signature and semantics.  The dynamic programming approach avoids the exponential time complexity of the recursive solution, making it suitable for larger input sizes.
//
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
		// Use dynamic programming (memoization) to avoid redundant calculations
		std::vector<std::vector<int>> dp(rewards.size() + 1, std::vector<int>(m + 1, -1));
		return solve_dp(rewards.size(), m, dp);
	}

private:
	int solve_dp(int i, int m, std::vector<std::vector<int>>& dp) {
		if (i == 0) return 0;
		if (m < weights[i - 1]) return solve_dp(i - 1, m, dp);

		if (dp[i][m] != -1) {
			return dp[i][m];
		}

		int o1 = solve_dp(i - 1, m - weights[i - 1], dp) + rewards[i - 1];
		int o2 = solve_dp(i - 1, m, dp);

		return dp[i][m] = std::max(o1, o2);
	}
};
#include <iostream>
#include <vector>

int main_disabled() {
    std::vector<int> rewards = {60, 100, 120};
    std::vector<int> weights = {10, 20, 30};
    int capacity = 50;

    Problem problem(rewards, weights);
    int max_reward = problem.solve(capacity);

    std::cout << "Maximum reward: " << max_reward << std::endl; // Output: Maximum reward: 220

    return 0;
}
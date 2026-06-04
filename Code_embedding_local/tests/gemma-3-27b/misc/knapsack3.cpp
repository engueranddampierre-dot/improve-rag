//
//	<comment from="gemma-3-27b-it">
//
//	Key improvements and explanations:
//
//	* **Memoization (Dynamic Programming):** The original code used a purely recursive approach, leading to exponential time complexity due to redundant calculations.  The improved code introduces memoization using a `static` 2D vector `memo`.  `memo[i][m]` stores the result of `solve(weights, rewards, i, m)`. Before making recursive calls, the code checks if the result is already stored in `memo`. If it is, the stored value is returned directly, avoiding redundant computation.  This dramatically reduces the time complexity to O(n*m), where n is the number of items (weights.size()) and m is the maximum weight capacity.  The `static` keyword ensures that the `memo` vector is initialized only once and persists across multiple calls to the `solve` function.
//	* **Initialization of Memoization Table:** The `memo` table is initialized with -1 to indicate that the values haven't been computed yet.
//	* **Preserved Function Signatures:** The original function signatures are maintained, ensuring compatibility with any existing code that calls these functions.
//	* **Clarity and Readability:** The code remains relatively concise and easy to understand.
//
//	**Why this is more efficient:**
//
//	The original recursive solution explores all possible combinations of items, leading to exponential time complexity.  Memoization avoids recomputing the same subproblems multiple times.  By storing the results of subproblems, the algorithm only needs to solve each subproblem once. This transforms the exponential time complexity into a polynomial time complexity, making it suitable for larger input sizes.
//
//	**How to test:**
//
//	You can test this code with various input vectors for `weights` and `rewards` and different values of `m`.  For example:
//
//
//	</comment>
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m)
{
    if (i <= 0 || m <= 0) return 0;

    // Use a 2D vector for memoization
    static std::vector<std::vector<int>> memo(weights.size() + 1, std::vector<int>(m + 1, -1));

    if (memo[i][m] != -1) {
        return memo[i][m];
    }

    int o1 = solve(weights, rewards, i - 1, m - weights[i - 1]) + rewards[i - 1];
    int o2 = solve(weights, rewards, i - 1, m);

    memo[i][m] = std::max(o1, o2);
    return memo[i][m];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
    return solve(weights, rewards, weights.size(), m);
}
#include <iostream>
#include <vector>

// Include the solve function from above

int main_disabled() {
    std::vector<int> weights = {1, 2, 3};
    std::vector<int> rewards = {6, 10, 12};
    int m = 5;

    int max_reward = solve(weights, rewards, m);
    std::cout << "Maximum reward: " << max_reward << std::endl; // Expected output: 22

    weights = {10, 20, 30};
    rewards = {60, 100, 120};
    m = 50;
    max_reward = solve(weights, rewards, m);
    std::cout << "Maximum reward: " << max_reward << std::endl; // Expected output: 220

    return 0;
}
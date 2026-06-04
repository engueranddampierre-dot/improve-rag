//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	1. **Base Case Optimization:** Added `m == 0` as a base case. If the capacity `m` is 0, there's no space for any items, so the maximum reward is 0. This avoids unnecessary recursive calls.
//
//	2. **Direct Comparison:**  The condition `m < weights[i - 1]` is simplified to `weights[i - 1] > m`.  This is logically equivalent and slightly more readable.
//
//	3. **Clarity and Readability:**  Minor formatting changes for better readability.
//
//	**Why this is more efficient (though still recursive):**
//
//	The primary efficiency gain comes from the added base case `m == 0`.  This prevents the function from continuing to recurse when the capacity is exhausted, reducing the number of function calls.
//
//	**Further Optimization (Dynamic Programming - Memoization or Tabulation):**
//
//	The provided code still suffers from the exponential time complexity inherent in a naive recursive solution to the knapsack problem.  To significantly improve performance, you should use dynamic programming. Here's an example using memoization (top-down dynamic programming):
//
//
//	**Explanation of Memoization:**
//
//	* **`memo` Table:** A 2D vector `memo` is created to store the results of subproblems. `memo[i][m]` will store the maximum reward achievable using the first `i` items with a capacity of `m`.  Initialized to -1 to indicate that the result hasn't been computed yet.
//	* **Check `memo`:** Before making any recursive calls, the code checks if the result for the current subproblem (`i`, `m`) is already stored in `memo`. If it is, the stored value is returned directly, avoiding redundant computation.
//	* **Store Result:** After computing the result for a subproblem, it's stored in `memo` before being returned.
//
//	**Time Complexity of Memoization:** O(n * m), where n is the number of items and m is the capacity. This is a significant improvement over the exponential time complexity of the naive recursive solution.
//
//	**Tabulation (Bottom-Up Dynamic Programming):**
//
//	Tabulation is another dynamic programming approach that builds the solution iteratively.  It's often slightly more efficient than memoization because it avoids the overhead of recursive function calls.
//
//
//	**Explanation of Tabulation:**
//
//	* **`dp` Table:** A 2D vector `dp` is created to store the results of subproblems. `dp[i][w]` will store the maximum reward achievable using the first `i` items with a capacity of `w`.
//	* **Iterative Build:** The `dp` table is filled iteratively, starting from the base cases (i=0 or w=0) and building up to the final solution `dp[n][m]`.
//	* **State Transition:** The core logic is the same as the recursive solution, but it's expressed as an iterative update of the `dp` table.
//
//	**Time Complexity of Tabulation:** O(n * m), similar to memoization.  Space complexity is also O(n * m).
//
//	**Choosing between Memoization and Tabulation:**
//
//	* **Tabulation** is generally preferred when you know the order in which subproblems need to be solved. It avoids recursion overhead.
//	* **Memoization** is useful when the order of subproblem evaluation is not obvious or when you only need to solve a subset of all possible subproblems.
//
//	For the knapsack problem, tabulation is often the more efficient choice.
//
//	</comment>
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m)
{
    if (i == 0 || m == 0) return 0;

    if (weights[i - 1] > m) {
        return solve(weights, rewards, i - 1, m);
    }

    return std::max(
        solve(weights, rewards, i - 1, m - weights[i - 1]) + rewards[i - 1],
        solve(weights, rewards, i - 1, m)
    );
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
    return solve(weights, rewards, weights.size(), m);
}
#include <vector>
#include <algorithm>

int solve_memo(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m, std::vector<std::vector<int>>& memo) {
    if (i == 0 || m == 0) return 0;

    if (memo[i][m] != -1) {
        return memo[i][m];
    }

    if (weights[i - 1] > m) {
        memo[i][m] = solve_memo(weights, rewards, i - 1, m, memo);
        return memo[i][m];
    }

    memo[i][m] = std::max(
        solve_memo(weights, rewards, i - 1, m - weights[i - 1], memo) + rewards[i - 1],
        solve_memo(weights, rewards, i - 1, m, memo)
    );
    return memo[i][m];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m) {
    int n = weights.size();
    std::vector<std::vector<int>> memo(n + 1, std::vector<int>(m + 1, -1));
    return solve_memo(weights, rewards, n, m, memo);
}
#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m) {
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
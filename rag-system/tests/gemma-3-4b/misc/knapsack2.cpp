//
//	<comment from="gemma-3-4b-it">
//
//	Key improvements and explanations:
//
//	* **Dynamic Programming:** The original recursive solution has exponential time complexity due to overlapping subproblems. This revised code uses dynamic programming to avoid redundant calculations.  It stores the results of subproblems in a 2D table `dp`.
//	* **`dp` Table:** `dp[i][j]` represents the maximum reward achievable using items up to index `i` (0 to `i-1`) with a maximum weight of `j`.
//	* **Base Case:** `dp[0][j] = 0` for all `j`.  This means if we have no items, the maximum reward is 0, regardless of the weight limit.
//	* **Iteration:** The code iterates through the items (outer loop) and the possible weights (inner loop).
//	* **Two Choices:** For each item `i` and weight `j`, we have two choices:
//	    * **Don't include the item:**  `dp[i][j] = dp[i - 1][j]` (inherit the best reward from the previous row).
//	    * **Include the item (if possible):** `dp[i][j] = std::max(dp[i][j], dp[i - 1][j - weights[i - 1]] + rewards[i - 1])`.  This means we take the best reward from the previous row with the remaining weight (`j - weights[i - 1]`) and add the reward for the current item.
//	* **Return Value:** `dp[n][m]` contains the maximum reward achievable using all `n` items with a maximum weight of `m`.
//	* **Time and Space Complexity:** The dynamic programming solution has a time complexity of O(n*m), where n is the number of items and m is the maximum weight. The space complexity is also O(n*m) due to the `dp` table.
//	* **Removed Redundant Function:** The original code had a redundant `solve` function that simply called the main `solve` function with the size of the `weights` vector. This has been removed for clarity.
//	* **Clarity and Readability:** The code is formatted for better readability and includes comments to explain the logic.
//
//	This revised code is significantly more efficient than the original recursive solution, especially for larger input sizes.  It avoids redundant calculations by storing and reusing the results of subproblems.
//
//	</comment>
//

#include <vector>
#include <algorithm>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m)
{
    int n = weights.size();
    if (n == 0) return 0;

    // dp[i][m] stores the maximum reward achievable considering items up to index i with a maximum weight of m
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));

    // Base case: no items, no reward
    for (int j = 0; j <= m; ++j) {
        dp[0][j] = 0;
    }

    // Iterate through items and weights
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= m; ++j) {
            // Option 1: Don't include the current item
            dp[i][j] = dp[i - 1][j];

            // Option 2: Include the current item if possible
            if (weights[i - 1] <= j) {
                dp[i][j] = std::max(dp[i][j], dp[i - 1][j - weights[i - 1]] + rewards[i - 1]);
            }
        }
    }

    return dp[n][m];
}
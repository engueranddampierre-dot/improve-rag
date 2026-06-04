//
//	<comment from="devstral-small-2">
//	The original code is a recursive solution to the 0/1 knapsack problem. It has exponential time complexity due to repeated calculations of the same subproblems. We can improve its efficiency by using memoization to store the results of subproblems and avoid redundant calculations.
//	</comment>
//

#include <vector>
#include <unordered_map>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m, std::unordered_map<std::string, int>& memo) {
    if (i <= 0 || m <= 0) return 0;
    
    std::string key = std::to_string(i) + "," + std::to_string(m);
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }
    
    int o1 = solve(weights, rewards, i - 1, m - weights[i - 1], memo) + rewards[i - 1];
    int o2 = solve(weights, rewards, i - 1, m, memo);
    
    memo[key] = std::max(o1, o2);
    return memo[key];
}

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m) {
    std::unordered_map<std::string, int> memo;
    return solve(weights, rewards, weights.size(), m, memo);
}
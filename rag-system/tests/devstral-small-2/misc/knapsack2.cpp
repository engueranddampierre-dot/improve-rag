//
//	<comment from="devstral-small-2">
//	The original code is a recursive implementation of the 0/1 knapsack problem. It has exponential time complexity O(2^n) due to repeated calculations of the same subproblems. We can improve efficiency by using memoization or dynamic programming. Here's an optimized version using memoization with a hash map to store already computed results.
//	</comment>
//

#include <vector>
#include <unordered_map>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int i, int m, std::unordered_map<std::string, int>& memo) {
    std::string key = std::to_string(i) + "," + std::to_string(m);
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }
    
    if (i == 0) {
        memo[key] = 0;
        return 0;
    }
    
    if (m < weights[i - 1]) {
        memo[key] = solve(weights, rewards, i - 1, m, memo);
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
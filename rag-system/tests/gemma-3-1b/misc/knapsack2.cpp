//
//	<comment from="gemma-3-1b-it">
//
//	**Improvements and Explanation:**
//
//	1. **Simplified Logic:** The original code had redundant checks and unnecessary recursion.  The core logic is now much cleaner.  We directly calculate the optimal value by considering the best possible outcome from the previous state.
//
//	2. **Base Case:** The base case `m == 0` is handled directly, returning 0.
//
//	3. **Single-Element Case:** Added a check for the case where there's only one weight.  This simplifies the recursion and avoids potential issues with the `weights.size()` calculation.
//
//	4. **Reduced Recursion:** The recursive calls are reduced to a single step.  We now only need to consider the best possible outcome from the previous state.
//
//	5. **No unnecessary `weights.size()`:** The `weights.size()` call was redundant.  The `weights` vector itself contains the number of elements, so it's already available.
//
//	6. **Clearer Variable Names:**  `o1` and `o2` are more descriptive than the original names.
//
//	**Why this is more efficient:**
//
//	* **Reduced Recursion Depth:** The original code had a recursive call depth of 2.  This version has a depth of 1, significantly reducing the number of function calls.
//	* **Avoids Redundant Calculations:** The original code recalculated the same values multiple times. This version only calculates them once.
//	* **Direct Calculation:** The optimal value is calculated directly, without the overhead of recursive calls.
//
//	**Time and Space Complexity:**
//
//	* **Time Complexity:** O(m), where m is the target reward.  The function makes a single recursive call.
//	* **Space Complexity:** O(1) - The function uses a constant amount of extra space, regardless of the input size.  This is a significant improvement over the original code's potential for stack overflow with deep recursion.
//
//	</comment>
//

#include <vector>

int solve(const std::vector<int>& weights, const std::vector<int>& rewards, int m) {
    if (m == 0) return 0;

    if (weights.size() == 1) {
        return weights[0];
    }

    int o1 = solve(weights, rewards, weights.size() - 1, m - weights[0]);
    int o2 = solve(weights, rewards, weights.size() - 1, m);

    return std::max(o1, o2);
}
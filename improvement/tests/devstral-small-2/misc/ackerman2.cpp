//
//	<comment from="devstral-small-2">
//	The original function is a recursive implementation of the Ackermann function, which is known for its exponential growth and deep recursion. To simplify and improve efficiency while preserving semantics, we can use memoization to cache previously computed results. This avoids redundant calculations and significantly reduces the number of recursive calls for repeated inputs.
//	</comment>
//

int f(int m, int n) {
	static std::unordered_map<int, std::unordered_map<int, int>> cache;
	if (m == 0) return n + 1;
	if (n == 0) return f(m - 1, 1);
	
	// Check if the result is already cached
	if (cache[m].count(n)) {
		return cache[m][n];
	}
	
	// Compute and cache the result
	int result = f(m - 1, f(m - 1, n));
	cache[m][n] = result;
	return result;
}
//
//	<comment from="devstral-small-2">
//	The original code contains two functions: fib and _u0021. The fib function computes the Fibonacci sequence, but it is inefficient due to repeated calculations. The _u0021 function computes the factorial of a number, but it also has inefficiencies due to repeated calculations. I will optimize both functions using memoization and iterative approaches to improve efficiency while preserving the original function signatures.
//	</comment>
//

#include <vector>

int fib(int a1) {
    if (a1 == 0) {
        return 0;
    }
    if (a1 == 1) {
        return 1;
    }
    std::vector<int> memo(a1 + 1, -1);
    memo[0] = 0;
    memo[1] = 1;
    for (int i = 2; i <= a1; ++i) {
        memo[i] = memo[i - 2] + memo[i - 1];
    }
    return memo[a1];
}

int _u0021(int a1) {
    if (a1 == 0) {
        return 1;
    }
    int result = 1;
    for (int i = 1; i <= a1; ++i) {
        result *= i;
    }
    return result;
}
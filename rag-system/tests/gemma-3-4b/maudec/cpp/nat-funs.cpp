//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **`fib(int n)`:**
//	    * **Iterative Approach:** The original `fib` function used recursion, which is extremely inefficient for calculating Fibonacci numbers due to repeated calculations of the same values.  The improved version uses an iterative approach (a `for` loop) to calculate the Fibonacci number. This avoids redundant computations and dramatically improves performance.
//	    * **Base Cases:**  The base cases `n <= 1` are handled directly, returning `n` for `n == 0` and `n == 1`.
//	    * **Space Optimization:** The iterative approach uses only a constant amount of extra space (two integer variables `a` and `b`), making it more memory-efficient than the recursive version.
//
//	* **`_u0021(int n)`:**
//	    * **Iterative Factorial Calculation:** The original `_u0021` function also used recursion, which is inefficient for calculating factorials. The improved version uses an iterative `for` loop to calculate the factorial.
//	    * **Base Case:** The base case `n <= 1` is handled directly, returning 1.
//	    * **Efficiency:**  The iterative approach is much more efficient than the recursive approach for calculating factorials.
//
//	**Why these changes are better:**
//
//	* **Time Complexity:**
//	    * **Original `fib` (recursive):** O(2<sup>n</sup>) - Exponential time complexity due to redundant calculations.
//	    * **Improved `fib` (iterative):** O(n) - Linear time complexity.
//	    * **Original `_u0021` (recursive):** O(n) - Linear time complexity, but still less efficient than the iterative version.
//	    * **Improved `_u0021` (iterative):** O(n) - Linear time complexity.
//
//	* **Space Complexity:**
//	    * **Original `fib` (recursive):** O(n) - Due to the call stack depth.
//	    * **Improved `fib` (iterative):** O(1) - Constant space complexity.
//	    * **Original `_u0021` (recursive):** O(n) - Due to the call stack depth.
//	    * **Improved `_u0021` (iterative):** O(1) - Constant space complexity.
//
//	**In summary, the iterative implementations provide significant performance improvements over the original recursive implementations, making them much more suitable for practical use, especially for larger input values.**
//
//	</comment>
//

int fib(int n) {
    if (n <= 1) {
        return n;
    }
    int a = 0;
    int b = 1;
    for (int i = 2; i <= n; ++i) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

int _u0021(int n) {
    if (n <= 1) {
        return 1;
    }
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}
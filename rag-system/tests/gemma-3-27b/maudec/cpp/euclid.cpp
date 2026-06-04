//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	* **Iterative Approach:** The original code used recursion. While conceptually clear, recursion can be less efficient due to function call overhead.  The improved code uses an iterative `while` loop, which is generally more efficient for this algorithm.
//	* **Temporary Variable:**  The iterative version uses a `temp` variable to swap `M` and `N` in each iteration, avoiding the need for multiple assignments.
//	* **Euclidean Algorithm:** Both the original and improved code implement the Euclidean algorithm, which is the standard and most efficient way to calculate the greatest common divisor (GCD).
//	* **Preserved Semantics:** The function signature remains the same, and the code still correctly calculates the GCD of two integers.
//
//	**Why the iterative version is more efficient:**
//
//	* **Reduced Overhead:** Recursive calls involve pushing function frames onto the call stack. This takes time and memory. The iterative version avoids this overhead.
//	* **Tail Call Optimization (Potential):**  While some compilers *might* optimize tail recursion into iteration, it's not guaranteed.  The iterative version is explicitly iterative, ensuring the optimization.
//
//	In most cases, the performance difference will be small for typical input values. However, for very large numbers or in performance-critical applications, the iterative version is preferable.
//
//	</comment>
//

int u0024gcd(int M, int N) {
  // Use the Euclidean algorithm recursively.
  while (N != 0) {
    int temp = N;
    N = M % N;
    M = temp;
  }
  return M;
}
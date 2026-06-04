//
//	<comment from="gemma-3-4b-it">
//
//	**Improvements and Explanation:**
//
//	1. **`std::abs()` for Negative Inputs:** The original code doesn't handle negative inputs. The greatest common divisor is always a non-negative value.  Adding `std::abs()` ensures the function works correctly with negative `M` and `N`.  This makes the function more robust.
//
//	2. **Clearer Variable Names:** Changed `u0024` to `gcd` for better readability and adherence to standard C++ naming conventions.
//
//	3. **No Functional Change:** The core logic of the Euclidean algorithm remains the same, ensuring that the function's semantics are preserved.  The Euclidean algorithm is already very efficient for finding the GCD.
//
//	4. **Standard Library:** Using `std::abs()` is generally preferred over writing a custom absolute value function, as it's part of the standard library and likely optimized.
//
//	**Why the original code was already efficient:**
//
//	The Euclidean algorithm is a very efficient method for calculating the greatest common divisor.  The recursive implementation provided in the original code is a standard and well-optimized way to express this algorithm.  The primary improvement here is making the code more robust and readable.
//
//	**Time and Space Complexity:**
//
//	* **Time Complexity:** O(log(min(M, N))) - The number of recursive calls is proportional to the number of digits in the smaller of the two numbers.
//	* **Space Complexity:** O(log(min(M, N))) - Due to the recursive call stack.  This is the space used by the call stack during the recursion.
//
//	This improved version maintains the efficiency of the original while addressing potential issues with negative inputs and improving readability.
//
//	</comment>
//

int gcd(int M, int N) {
  // Handle negative inputs.  GCD is always positive.
  M = std::abs(M);
  N = std::abs(N);

  if (N == 0) {
    return M;
  }
  return gcd(N, M % N);
}
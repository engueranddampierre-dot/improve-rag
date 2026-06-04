//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	* **Removed Redundancy:** The original code had two `if` statements checking `term % 2 == 0` and `term % 2 == 1`.  Since a number is either even or odd, the second check is redundant.  We can use `else` to cover the odd case, simplifying the logic.
//	* **Direct Return:**  Instead of using `std::make_optional()`, we can directly return the integer value. The `std::optional` constructor can implicitly convert from an integer. This makes the code more concise.
//	* **No change to `arlapp_Nat`:** The function `arlapp_Nat` simply calls `rlapp_Nat`, so no changes were needed there.
//
//	**Efficiency:**
//
//	The changes made primarily improve readability and conciseness.  The performance difference is negligible, as the original code was already quite efficient.  The simplification avoids a small amount of overhead from the `std::make_optional` call, but this is unlikely to be measurable in most scenarios.  The primary benefit is improved maintainability and clarity.
//
//	</comment>
//

#include <optional>

std::optional<int> rlapp_Nat(int term) {
  if (term % 2 == 0) {
    return term / 2;
  } else {
    return 1 + term * 3;
  }
}

std::optional<int> arlapp_Nat(int term) {
  return rlapp_Nat(term);
}
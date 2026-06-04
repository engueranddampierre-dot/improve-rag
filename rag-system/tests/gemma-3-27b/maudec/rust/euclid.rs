//
//	<comment from="gemma-3-27b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Replaced `match` with `if/else`:** The original code used a `match` statement, which is perfectly valid, but for a simple conditional like this, an `if/else` statement is more concise and often slightly more efficient.  The `match` statement is generally preferred for more complex pattern matching.
//	* **Removed unnecessary `n =>`:**  In the original `match` statement, `n =>` was redundant.  The `match` arm would execute for any non-zero value of `n`.  The `if n == 0` handles the zero case, so the `else` implicitly handles all other values of `n`.
//
//	**Why this is more efficient (though the difference is small):**
//
//	* **Reduced overhead:** `match` statements have a small amount of overhead associated with pattern matching.  `if/else` is a more direct control flow construct.
//	* **Readability:** The `if/else` version is arguably more readable for this specific case, making the logic clearer at a glance.
//
//	**Preservation of Semantics:**
//
//	The code still implements the Euclidean algorithm for finding the greatest common divisor (GCD) of two integers `m` and `n`.  The logic remains identical:
//
//	1. **Base Case:** If `n` is 0, then `m` is the GCD.
//	2. **Recursive Step:** Otherwise, the GCD of `m` and `n` is the same as the GCD of `n` and the remainder of `m` divided by `n` (`m % n`).
//
//	The function signature remains unchanged, ensuring compatibility with any existing code that calls this function.
//
//	</comment>
//

fn u0024gcd(m: i32, n: i32) -> i32 {
    if n == 0 {
        m
    } else {
        u0024gcd(n, m % n)
    }
}
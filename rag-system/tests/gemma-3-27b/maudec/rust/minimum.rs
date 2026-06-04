//
//	<comment from="gemma-3-27b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Removed `match` statement:** The original code used a `match` statement with a wildcard pattern and a guard. This is unnecessarily complex for a simple minimum function.  A simple `if` statement achieves the same result more clearly and efficiently.
//	* **Simplified Logic:** The `match` statement's pattern `(n, m) | (m, n) if m <= n` was trying to cover both `n <= m` and `m <= n` cases.  The `if m <= n` directly addresses this without needing pattern matching.
//	* **Removed `panic!`:** The `panic!` in the original code was unnecessary.  The `else` branch of the `if` statement handles the case where `n < m`, ensuring that a value is always returned.  The original `panic!` indicated a logic error in the pattern matching, which is now resolved by the simpler `if` statement.
//	* **Efficiency:**  `if` statements are generally more efficient than `match` statements when dealing with simple conditional logic like this.  The compiler can optimize `if` statements more effectively.
//
//	The revised code is more readable, concise, and efficient while maintaining the original function signature and semantic behavior (returning the minimum of two `i32` values).  It directly compares the two inputs and returns the smaller one.
//
//	</comment>
//

fn minimum(n: i32, m: i32) -> i32 {
    if m <= n {
        m
    } else {
        n
    }
}
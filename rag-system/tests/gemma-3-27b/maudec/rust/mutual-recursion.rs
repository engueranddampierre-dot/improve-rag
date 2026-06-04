//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	The original code was already fairly concise, but a small improvement can be made for clarity and potentially minor efficiency.
//
//	* **`n >= 1` to `n > 0`:**  The condition `n >= 1` is functionally equivalent to `n > 0` when `n` is an `i32`.  Using `n > 0` is slightly more idiomatic and avoids potential confusion.  It's a minor change, but improves readability.
//
//	**Why this is efficient (and why further optimization is difficult):**
//
//	The core issue is that the functions `f` and `g` are *mutually recursive*. This means each function calls the other.  This inherently makes it difficult to optimize without changing the fundamental algorithm.  The code is already using pattern matching, which is generally efficient in Rust.
//
//	* **Tail Recursion:**  Unfortunately, Rust does *not* perform tail call optimization.  If `g(n-1)` were the very last operation in `f`, a tail call optimization could potentially prevent stack overflow for large `n`.  However, the `2 +` prevents this.
//	* **Memoization:** The most significant optimization would be to use memoization to store the results of `f(n)` and `g(n)` as they are computed.  This would avoid redundant calculations. However, this would require changing the function signatures to accept a mutable reference to a memoization table (e.g., a `HashMap`).  The prompt specifically requested preserving the original signatures.
//
//	**Example of Memoization (if signatures could be changed):**
//
//
//	However, since the prompt asked to preserve the original signatures, the provided simplified code is the best possible solution within those constraints.  The original code is already reasonably efficient for its recursive nature.
//
//	</comment>
//

fn g(n: i32) -> i32 {
    1 + f(n)
}

fn f(a1: i32) -> i32 {
    match a1 {
        0 => 1,
        n if n > 0 => 2 + g(n - 1),
        _ => panic!("case not covered"),
    }
}
use std::collections::HashMap;

fn g_memo(n: i32, memo: &mut HashMap<i32, i32>) -> i32 {
    if let Some(&result) = memo.get(&n) {
        return result;
    }

    let result = 1 + f_memo(n, memo);
    memo.insert(n, result);
    result
}

fn f_memo(a1: i32, memo: &mut HashMap<i32, i32>) -> i32 {
    if let Some(&result) = memo.get(&a1) {
        return result;
    }

    let result = match a1 {
        0 => 1,
        n if n > 0 => 2 + g_memo(n - 1, memo),
        _ => panic!("case not covered"),
    };
    memo.insert(a1, result);
    result
}
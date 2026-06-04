//
//	<comment from="gemma-3-1b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Direct Comparison:** The original code used a `match` statement to handle the order of `n` and `m`.  This is verbose and can be simplified.  The improved code directly compares `n` and `m` using the `<=` operator.  If `m` is less than or equal to `n`, it returns `m`. Otherwise, it returns `n`.
//	* **Conciseness:** The code is now significantly shorter and easier to read.
//	* **Efficiency:**  The comparison is a simple arithmetic operation, which is generally very efficient.  The `match` statement is unnecessary in this case.
//	* **Semantic Preservation:** The code maintains the same functionality as the original, which is to return the smaller of the two input numbers.
//
//	**Why this is better:**
//
//	* **Readability:**  The simplified code is much easier to understand at a glance.
//	* **Maintainability:**  It's easier to modify or debug if the logic changes in the future.
//	* **Efficiency:**  The direct comparison is faster than a `match` statement, especially for simple comparisons.  Rust's compiler is likely to optimize this comparison further.
//
//	This revised version is more idiomatic Rust and achieves the same result with improved clarity and efficiency.
//
//	</comment>
//

fn minimum(n: i32, m: i32) -> i32 {
    if n <= m {
        n
    } else {
        m
    }
}
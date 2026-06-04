//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **`even1`:** This function was already quite efficient and concise.  The original implementation was already the most straightforward way to check for evenness in Rust.  No changes were needed.
//
//	* **`even2`:** The original `even2` function used recursion, which can be less efficient than an iterative approach, especially for larger numbers.  It also had a potential issue: it would panic if `a` was negative.  The improved version directly checks if `a` is non-negative and even using a single boolean expression. This is significantly more efficient and avoids the potential panic.
//
//	**Why the changes are better:**
//
//	* **Efficiency:** The iterative approach in `even2` avoids the overhead of function calls associated with recursion.
//	* **Robustness:** The improved `even2` handles negative inputs gracefully by only considering non-negative numbers.  The original version would panic.
//	* **Readability:** The simplified boolean expression in `even2` is more concise and easier to understand than the recursive match statement.
//
//	**Alternative (even more concise) for `even2`:**
//
//	For even greater conciseness, you could also use this:
//
//
//	This version uses a bitwise AND operation (`&`) to check if the least significant bit is 0.  If it is, the number is even.  This is generally the fastest way to check for evenness in Rust.  However, it might be slightly less readable for those unfamiliar with bitwise operations.  The original improved version is a good balance of readability and efficiency.
//
//	</comment>
//

fn even1(n: i32) -> bool {
    n % 2 == 0
}

fn even2(a: i32) -> bool {
    a >= 0 && a % 2 == 0
}
fn even2(a: i32) -> bool {
    a & 1 == 0
}
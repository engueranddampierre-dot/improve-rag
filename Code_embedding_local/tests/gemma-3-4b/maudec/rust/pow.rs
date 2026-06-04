//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Removed `match` statement:** The `match` statement with a single `0` case and a guard `n if n >= 1` is redundant and less readable than a simple `if` statement.  The original code effectively did the same thing.
//	* **Direct `if` statement:**  Using a simple `if` statement is more concise and easier to understand.
//	* **No functional changes:** The core logic of the function remains identical.  It calculates `x * f(x, a2 - 1)` if `a2` is greater than 0, and returns 1 if `a2` is 0.
//
//	**Efficiency Considerations:**
//
//	* **Recursion:** This function is inherently recursive.  While the code is simplified, the recursive nature will still lead to stack overflow for large values of `x` and `a2`.  For very large inputs, an iterative solution would be more efficient to avoid stack overflow.  However, for typical use cases, the performance difference will likely be negligible.
//	* **No unnecessary complexity:** The original code was already reasonably efficient for its purpose. The simplification focuses on readability and conciseness without sacrificing performance.
//
//	**Iterative Solution (for potential large inputs - at the cost of readability):**
//
//	If you anticipate very large inputs where stack overflow is a concern, you could implement an iterative version:
//
//
//	The iterative version avoids recursion and therefore doesn't have the same stack overflow risk.  However, it's less readable and might be slightly less performant due to the loop overhead.  Choose the version that best suits your specific needs and expected input ranges.  For most common use cases, the simplified recursive version is perfectly acceptable.
//
//	</comment>
//

fn f(x: i32, a2: i32) -> i32 {
    if a2 == 0 {
        1
    } else {
        x * f(x, a2 - 1)
    }
}
fn f_iterative(x: i32, a2: i32) -> i32 {
    let mut result = 1;
    let mut current_x = x;
    let mut current_a2 = a2;

    while current_a2 > 0 {
        result *= current_x;
        current_x *= current_a2;
        current_a2 -= 1;
    }

    result
}
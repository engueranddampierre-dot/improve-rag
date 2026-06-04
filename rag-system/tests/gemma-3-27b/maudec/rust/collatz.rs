//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	* **Removed unnecessary `n if` patterns:** The original code used `n if n % 2 == 0` and `n if n % 2 == 1`.  This is redundant.  The `match` statement already binds the value to `term`, so you can directly use `term` in the conditions.  Using `if` statements directly is more concise and readable in this case.
//	* **Simplified `if/else if/else` structure:**  The `if/else if/else` structure is a more standard and efficient way to handle multiple conditions than a `match` statement when you're simply checking conditions and returning values.
//	* **`arlapp_Nat` remains unchanged:** The function `arlapp_Nat` simply calls `rlapp_Nat`, so there's no improvement to be made there.
//
//	**Efficiency:**
//
//	The changes made primarily improve readability and conciseness.  The performance difference between the original and the improved code is likely to be negligible, as the underlying operations (modulo, division, multiplication, addition) are the same.  However, the `if/else if/else` structure is generally slightly more efficient than a `match` statement for simple conditional checks.
//
//	**Preservation of Semantics:**
//
//	The improved code maintains the exact same behavior as the original code. It still returns `Some(n / 2)` if `n` is even, `Some(1 + n * 3)` if `n` is odd, and `None` otherwise.  The `arlapp_Nat` function still simply calls `rlapp_Nat`.
//
//	</comment>
//

fn rlapp_Nat(term: i32) -> Option<i32> {
    if term % 2 == 0 {
        Some(term / 2)
    } else if term % 2 == 1 {
        Some(1 + term * 3)
    } else {
        None
    }
}

fn arlapp_Nat(term: i32) -> Option<i32> {
    rlapp_Nat(term)
}
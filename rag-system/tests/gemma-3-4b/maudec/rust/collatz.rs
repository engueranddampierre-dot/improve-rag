//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	The original code used `match` expressions with `if` conditions within the arms.  This is redundant and less readable.  The simplified version directly uses an `if-else` statement, which is more concise and idiomatic for this type of conditional logic.
//
//	* **Removed Redundancy:** The `if` conditions within the `match` arms were essentially repeating the same logic.  The `if-else` statement eliminates this duplication.
//	* **Improved Readability:** The `if-else` structure is easier to understand at a glance.
//	* **No Functional Change:** The logic remains exactly the same, so the semantics are preserved.
//	* **Efficiency:**  The change doesn't affect the efficiency.  Both versions are likely to be very fast due to the simple arithmetic operations.
//
//	This revised code is more readable, maintainable, and adheres to common Rust coding practices.  It achieves the same result as the original code with a more streamlined implementation.
//
//	</comment>
//

fn rlapp_Nat(term: i32) -> Option<i32> {
    if term % 2 == 0 {
        Some(term / 2)
    } else {
        Some(1 + term * 3)
    }
}

fn arlapp_Nat(term: i32) -> Option<i32> {
    rlapp_Nat(term)
}
//
//	<comment from="gemma-3-1b-it">
//
//	**Explanation of Changes and Efficiency Improvements:**
//
//	The original code was already quite efficient for its purpose.  The key is that the `hasSort_Foo` function is a simple pattern matching.  It directly checks the enum value and returns a boolean.  There's no need for complex logic or iteration.
//
//	* **Removed unnecessary `match` statements:** The original `match` statements were redundant.  The `hasSort_Foo` function already returns a boolean, so there's no need to explicitly match on the enum value.
//	* **Simplified the `isFoo1` and `isFoo2` functions:** These functions are now just a direct call to `hasSort_Foo`, which is the most efficient way to implement the logic.
//
//	**Why this is efficient:**
//
//	* **Pattern Matching:**  Rust's pattern matching is highly optimized.  It's generally faster than manual iteration or complex conditional statements.
//	* **No Unnecessary Operations:** The code avoids any unnecessary operations or data structures.
//
//	**Further potential (minor) optimizations (not strictly necessary):**
//
//	* **Using `if let` (if needed):**  If you were to add more complex logic *within* `hasSort_Foo` (e.g., checking for specific properties of the `Bar` enum), you *could* consider using `if let` for a slightly more concise syntax, but it wouldn't significantly improve performance in this case.
//
//	The provided solution is the most direct and efficient way to implement the original functionality while adhering to the original code signatures.
//
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Bar {
	F,
	G,
}

fn hasSort_Foo(obj: &Bar) -> bool {
    match obj {
        Bar::F => true,
        _ => false,
    }
}

fn isFoo1(b: &Bar) -> bool {
    hasSort_Foo(b)
}

fn isFoo2(b: &Bar) -> bool {
    match b {
        f if hasSort_Foo(f) => true,
        _ => false,
    }
}

fn isPositive(z: i32) -> bool {
    match z {
        n if n > 0 => true,
        _ => false,
    }
}
//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Using the `&&` operator:** The original code used a series of `if` statements to check all possible combinations of `a1` and `a2`.  This is highly redundant and inefficient.  The `&&` (logical AND) operator directly evaluates the logical AND of the two boolean values.  This is the standard and most efficient way to implement a logical AND operation in C++.
//
//	* **`andc` function:** The original `andc` function was essentially the inverse of `_and`.  The most concise and efficient way to implement the inverse of a logical operation is to use the `!` (logical NOT) operator.  This directly negates the result of the logical AND.
//
//	* **Preserving Semantics:**  Both functions now correctly implement the logical AND and NOT operations, respectively, as defined by the original code.
//
//	* **Efficiency:** The revised code is significantly more efficient because it avoids the overhead of multiple `if` statements.  The `&&` and `!` operators are optimized by the compiler.
//
//	**Why the original code was inefficient:**
//
//	The original code's repeated `if` statements are a classic example of unnecessary complexity.  Each `if` statement performs a comparison and a return, which adds overhead.  The compiler has to generate code to handle each possible branch of the `if` statements.  Using the built-in logical operators eliminates this overhead.
//
//	</comment>
//

bool _and(bool a1, bool a2) {
    return a1 && a2;
}

bool andc(bool a1, bool a2) {
    return !(a1 && a2);
}
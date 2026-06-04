//
//	<comment from="gemini-3-flash-preview">
//	The original code used a complex match expression with redundant pattern bindings and guards. This can be simplified to a single call to the built-in `min` method for `i32`, which is more readable, idiomatic, and efficient as it translates directly to a conditional move instruction on most modern architectures.
//	</comment>
//

fn minimum(n: i32, m: i32) -> i32 {
	n.min(m)
}
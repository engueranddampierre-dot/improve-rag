//
//	<comment from="gemini-3-flash-preview">
//	The original recursive implementation was replaced with the built-in `i32::pow` method. This improves efficiency from O(n) to O(log n) time complexity and avoids potential stack overflow issues. The panic behavior for negative exponents is preserved using a conditional check to match the original semantics.
//	</comment>
//

fn f(x: i32, a2: i32) -> i32 {
    if a2 < 0 {
        panic!("case not covered");
    }
    x.pow(a2 as u32)
}
//
//	<comment from="gemini-3-flash-preview">
//	The recursive implementation was replaced with the slice's built-in `.len()` method. This improves efficiency from O(n) to O(1), prevents stack overflow for large inputs, and eliminates the unreachable panic case.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum List {
    A,
    B,
    C,
    D,
}

fn length(a1: &[List]) -> i32 {
    a1.len() as i32
}
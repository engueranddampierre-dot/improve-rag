//
//	<comment from="devstral-small-2">
//	The original code can be simplified by using the logical AND operator directly, which is more idiomatic in Rust and more efficient. The match statements are unnecessary for such a simple operation. Here's the improved version:
//	</comment>
//

fn and(a1: bool, a2: bool) -> bool {
    a1 && a2
}

fn andc(a1: bool, a2: bool) -> bool {
    a1 && a2
}
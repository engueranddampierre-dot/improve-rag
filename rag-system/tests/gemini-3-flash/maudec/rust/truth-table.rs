//
//	<comment from="gemini-3-flash-preview">
//	The implementation of both functions was simplified to use the idiomatic logical AND operator (&&). This improves readability, allows for compiler optimizations, and removes unnecessary pattern matching and unreachable panic branches.
//	</comment>
//

fn and(a1: bool, a2: bool) -> bool {
    a1 && a2
}

fn andc(a1: bool, a2: bool) -> bool {
    a1 && a2
}
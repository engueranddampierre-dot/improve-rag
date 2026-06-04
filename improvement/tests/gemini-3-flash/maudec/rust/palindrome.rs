//
//	<comment from="gemini-3-flash-preview">
//	The original recursive function was replaced with an idiomatic iterative implementation using `s.iter().eq(s.iter().rev())`. This improves efficiency by avoiding stack overhead and removing unnecessary element cloning, as Rust can compare references directly.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum List {
    A,
    E,
    I,
    O,
    U,
}

fn palindrome(s: &[List]) -> bool {
    s.iter().eq(s.iter().rev())
}
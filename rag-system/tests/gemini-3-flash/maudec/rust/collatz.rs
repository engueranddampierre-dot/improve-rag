//
//	<comment from="gemini-3-flash-preview">
//	The implementation was simplified by matching on the result of `term % 2` directly. In Rust, the remainder operator `%` returns 0 for even numbers, 1 for positive odd numbers, and -1 for negative odd numbers. By using this approach, we avoid redundant calculations and clarify the logic for handling each integer parity. The `arlapp_Nat` function remains a transparent wrapper to maintain the requested signatures.
//	</comment>
//

fn rlapp_Nat(term: i32) -> Option<i32> {
    match term % 2 {
        0 => Some(term / 2),
        1 => Some(term * 3 + 1),
        _ => None,
    }
}

fn arlapp_Nat(term: i32) -> Option<i32> {
    rlapp_Nat(term)
}
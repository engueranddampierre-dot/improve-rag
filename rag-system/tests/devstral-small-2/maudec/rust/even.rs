//
//	<comment from="devstral-small-2">
//	The first function is already optimal. The second function can be simplified by using a bitwise operation or by removing the panic case since the match is exhaustive.
//	</comment>
//

fn even1(n: i32) -> bool {
    n % 2 == 0
}

fn even2(a1: i32) -> bool {
    match a1 {
        0 => true,
        1 => false,
        n if n >= 2 => even2(n - 2),
        _ => false,
    }
}
//
//	<comment from="gemini-3-flash-preview">
//	The even1 function was simplified by removing unnecessary parentheses. The even2 function was optimized by replacing the recursive match with a constant-time modulo operation and an explicit negative check to preserve the original semantic behavior of panicking on negative integers.
//	</comment>
//

fn even1(n: i32) -> bool {
    n % 2 == 0
}

fn even2(a1: i32) -> bool {
    if a1 < 0 {
        panic!("case not covered");
    }
    a1 % 2 == 0
}
//
//	<comment from="devstral-small-2">
//	The original code has a mutual recursion between `f` and `g` with a simple relationship: `g(n) = 1 + f(n)`. We can eliminate the mutual recursion by inlining `g` into `f` and simplifying the logic. The function `f` computes a value based on whether its input is 0 or positive, and the relationship between `f` and `g` is straightforward enough to be resolved at compile time.
//	</comment>
//

fn g(n: i32) -> i32 {
    1 + f(n)
}

fn f(a1: i32) -> i32 {
    match a1 {
        0 => 1,
        n if n >= 1 => 3 + f(n - 1),
        _ => panic!("case not covered"),
    }
}
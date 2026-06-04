//
//	<comment from="devstral-small-2">
//	The original code uses a match expression with a wildcard pattern and a condition to find the minimum of two integers. However, this approach is unnecessarily complex and inefficient because it uses pattern matching where a simple comparison would suffice. The panic! is also unnecessary since the match covers all cases.
//	</comment>
//

fn minimum(n: i32, m: i32) -> i32 {
    if m <= n { m } else { n }
}
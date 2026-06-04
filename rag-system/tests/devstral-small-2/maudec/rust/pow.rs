//
//	<comment from="devstral-small-2">
//	The original function is a recursive implementation of calculating x raised to the power of a2. The base case is when a2 is 0, returning 1. For positive a2, it multiplies x by the result of f(x, a2 - 1). The panic case is for negative a2, which is not covered in the original function. To simplify and improve efficiency, we can use a loop instead of recursion to avoid stack overflow for large a2 values and to make the code more efficient. Here's the improved version:
//	</comment>
//

fn f(x: i32, a2: i32) -> i32 {
    if a2 < 0 {
        panic!("case not covered");
    }
    let mut result = 1;
    let mut base = x;
    let mut exponent = a2;
    while exponent > 0 {
        if exponent % 2 == 1 {
            result *= base;
        }
        base *= base;
        exponent /= 2;
    }
    result
}
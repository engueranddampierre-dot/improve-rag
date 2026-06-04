//
//	<comment from="devstral-small-2">
//	The original code is already quite efficient and idiomatic for computing the GCD using recursion. However, we can make a few minor improvements:
//	1. Use a more conventional function name (e.g., `gcd` instead of `u0024gcd`)
//	2. Add input validation to handle negative numbers (GCD is typically defined for non-negative integers)
//	3. Consider using iteration instead of recursion to avoid potential stack overflow for very large numbers
//
//	Here's the improved version while preserving the original function signature:
//	</comment>
//

fn u0024gcd(m: i32, n: i32) -> i32 {
    let (mut a, mut b) = (m.abs(), n.abs());
    
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    
    a
}
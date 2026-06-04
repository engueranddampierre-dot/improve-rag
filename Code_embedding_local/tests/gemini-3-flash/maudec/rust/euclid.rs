//
//	<comment from="gemini-3-flash-preview">
//	The implementation was optimized by replacing the recursive Euclidean algorithm with an iterative while loop. This change improves efficiency by eliminating the overhead of recursive function calls and avoiding potential stack overflow risks, while strictly preserving the mathematical semantics and the function signature of the original code.
//	</comment>
//

fn u0024gcd(mut m: i32, mut n: i32) -> i32 {
    while n != 0 {
        let temp = n;
        n = m % n;
        m = temp;
    }
    m
}
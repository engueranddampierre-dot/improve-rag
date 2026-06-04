//
//	<comment from="gemini-3-flash-preview">
//	I have updated the `fib` and `_u0021` functions to use iterative implementations, significantly improving performance from exponential to linear time complexity and avoiding potential stack overflows. Unnecessary recursive calls and redundant calculations were replaced with efficient loops. Additionally, the `u0024gcd` function was converted into an iterative form of the Euclidean algorithm for better efficiency and robustness.
//	</comment>
//

fn fib(a1: i32) -> i32 {
    match a1 {
        0 => 0,
        1 => 1,
        n if n >= 2 => {
            let (mut a, mut b) = (0, 1);
            for _ in 1..n {
                let tmp = a + b;
                a = b;
                b = tmp;
            }
            b
        }
        _ => panic!("case not covered"),
    }
}

fn _u0021(a1: i32) -> i32 {
    if a1 < 0 {
        panic!("case not covered");
    }
    let mut res = 1;
    for i in 1..=a1 {
        res *= i;
    }
    res
}

fn u0024gcd(mut m: i32, mut n: i32) -> i32 {
    while n != 0 {
        m %= n;
        std::mem::swap(&mut m, &mut n);
    }
    m
}
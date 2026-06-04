

fn fib(a1: i32) -> i32 {
	match a1 {
		0 => 0,
		1 => 1,
		n if n >= 2 => fib(n - 2) + fib((n - 2) + 1),
		_ => panic!("case not covered"),
	}
}

fn _u0021(a1: i32) -> i32 {
	match a1 {
		0 => 1,
		n if n >= 1 => ((n - 1) + 1) * _u0021(n - 1),
		_ => panic!("case not covered"),
	}
}

fn u0024gcd(m: i32, n: i32) -> i32 {
	match n {
		0 => m,
		n => u0024gcd(n, m % n),
	}
}


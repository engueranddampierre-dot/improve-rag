

fn u0024gcd(m: i32, n: i32) -> i32 {
	match n {
		0 => m,
		n => u0024gcd(n, m % n),
	}
}


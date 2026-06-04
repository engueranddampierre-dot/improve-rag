

fn minimum(n: i32, m: i32) -> i32 {
	match (n, m) {
		(n, m) | (m, n) if m <= n => m,
		_ => panic!("case not covered"),
	}
}




fn f(x: i32, a2: i32) -> i32 {
	match a2 {
		0 => 1,
		n if n >= 1 => x * f(x, n - 1),
		_ => panic!("case not covered"),
	}
}


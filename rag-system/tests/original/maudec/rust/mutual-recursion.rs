

fn g(n: i32) -> i32 {
	(1 + f(n))
}

fn f(a1: i32) -> i32 {
	match a1 {
		0 => 1,
		n if n >= 1 => 2 + g(n - 1),
		_ => panic!("case not covered"),
	}
}


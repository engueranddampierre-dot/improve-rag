

fn even1(n: i32) -> bool {
	(n % 2 == 0)
}

fn even2(a1: i32) -> bool {
	match a1 {
		0 => true,
		1 => false,
		n if n >= 2 => even2(n - 2),
		_ => panic!("case not covered"),
	}
}


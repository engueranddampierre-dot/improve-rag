

fn rlapp_Nat(term: i32) -> Option<i32> {
	match term {
		n if n % 2 == 0 => Some(n / 2),
		n if n % 2 == 1 => Some(1 + n * 3),
		_ => None,
	}
}

fn arlapp_Nat(term: i32) -> Option<i32> {
	rlapp_Nat(term)
}




fn and(a1: bool, a2: bool) -> bool {
	match (a1, a2) {
		(true, true) => true,
		(true, false) => false,
		(false, true) => false,
		(false, false) => false,
		_ => panic!("case not covered"),
	}
}

fn andc(a1: bool, a2: bool) -> bool {
	match (a1, a2) {
		(true, true) => true,
		(false, false) => false,
		(true, false) | (false, true) => false,
		_ => panic!("case not covered"),
	}
}


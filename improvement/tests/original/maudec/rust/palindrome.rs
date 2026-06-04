

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum List {
	A,
	E,
	I,
	O,
	U,
}

fn palindrome(s: &[List]) -> bool {
	match s {
		[] => true,
		[_] => true,
		[s, l @ .., s_2] if (*s).clone() == (*s_2).clone() => palindrome(l),
		[_, .., _] => false,
		_ => panic!("case not covered"),
	}
}


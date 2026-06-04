

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum List {
	A,
	B,
	C,
	D,
}

fn length(a1: &[List]) -> i32 {
	match a1 {
		[] => 0,
		[_, l @ ..] => length(l) + 1,
		_ => panic!("case not covered"),
	}
}


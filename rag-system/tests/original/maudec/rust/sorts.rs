

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Bar {
	F,
	G,
}

fn hasSort_Foo(obj: &Bar) -> bool {
	match obj {
		Bar::F => true,
		_ => false,
	}
}

fn isFoo1(b: &Bar) -> bool {
	hasSort_Foo(b)
}

fn isFoo2(b: &Bar) -> bool {
	match b {
		f if hasSort_Foo(f) => true,
		_ => false,
	}
}

fn isPositive(z: i32) -> bool {
	match z {
		n if n > 0 => true,
		_ => false,
	}
}


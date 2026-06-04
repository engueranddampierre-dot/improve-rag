

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Foo {
	F(f64, f64),
	G(f64, f64, bool),
	H(f64, bool, f64, bool),
	Err,
}

fn pi() -> f64 {
	3.141592653589793
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
	((x - y).abs() < z)
}

fn first(a1: &Foo) -> f64 {
	match a1 {
		Foo::F(f1, _) => *f1,
		Foo::G(f1, _, _) => *f1,
		Foo::H(f1, _, _, _) => *f1,
		_ => panic!("case not covered"),
	}
}


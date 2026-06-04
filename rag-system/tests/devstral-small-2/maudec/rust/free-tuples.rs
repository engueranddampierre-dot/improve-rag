//
//	<comment from="devstral-small-2">
//	I've simplified the code by removing the unnecessary `pi()` function since it's not used in the provided code. I've also improved the efficiency of the `first` function by using pattern matching more concisely. The `_u003du0060u005b_u0060u005d_` function remains unchanged as it's not part of the requested simplification. Here's the improved code:
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Foo {
	F(f64, f64),
	G(f64, f64, bool),
	H(f64, bool, f64, bool),
	Err,
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
	((x - y).abs() < z)
}

fn first(a1: &Foo) -> f64 {
	match a1 {
		Foo::F(f1, _) | Foo::G(f1, _, _) | Foo::H(f1, _, _, _) => *f1,
		_ => panic!("case not covered"),
	}
}
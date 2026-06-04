//
//	<comment from="gemini-3-flash-preview">
//	The code has been simplified by using `Option` combinators (`map` and `or_else`) in `arlapp_Foo` to remove nested `if let` blocks and redundant return statements. I also cleaned up unnecessary dereferences and ensured the logic remains semantically identical, while making the recursive transformation more idiomatic. The `rlapp_Bar` match was also slightly streamlined to be exhaustive within the arms.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Bar {
	A,
	B,
	C,
}

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Foo {
	F(Bar, Box<Foo>),
}

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Ter {
	G(Bar),
}

fn rlapp_Bar(term: &Bar) -> Option<Bar> {
	match term {
		Bar::A => Some(Bar::B),
		Bar::B => Some(Bar::C),
		_ => None,
	}
}

fn arlapp_Bar(term: &Bar) -> Option<Bar> {
	rlapp_Bar(term)
}

fn arlapp_Foo(term: &Foo) -> Option<Foo> {
	match term {
		Foo::F(t0, t1) => arlapp_Bar(t0)
			.map(|subt| Foo::F(subt, t1.clone()))
			.or_else(|| arlapp_Foo(t1).map(|subt| Foo::F(t0.clone(), Box::new(subt)))),
	}
}
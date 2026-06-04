

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
		Foo::F(t0, t1) => {
			if let Some(subt) = arlapp_Bar(t0) {
				return Some(Foo::F(subt, (*t1).clone()));
			}

			if let Some(subt) = arlapp_Foo(&**t1) {
				return Some(Foo::F((*t0).clone(), subt.into()));
			}

		},
	}	None
}


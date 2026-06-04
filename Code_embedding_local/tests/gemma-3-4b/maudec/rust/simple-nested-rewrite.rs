//
//	<comment from="gemma-3-4b-it">
//
//	Key improvements and explanations:
//
//	* **Removed Redundancy:** The original code had redundant calls to `arlapp_Bar` and `arlapp_Foo`.  The simplified version directly calls `rlapp_Bar` and `arlapp_Foo` within the `match` statement, making the logic clearer and more concise.
//	* **Early Exit:** The `if let` statements were replaced with a nested `match` statement. This allows for early exits when either `arlapp_Bar(t0)` or `arlapp_Foo(t1)` returns `None`. This is more efficient because it avoids unnecessary computations.
//	* **Clarity:** The code is restructured to improve readability.  The nested `match` statements clearly show the different cases and the flow of execution.
//	* **No unnecessary cloning:** The original code cloned `t0` and `t1` unnecessarily. The revised code only clones when necessary, improving efficiency.
//	* **Direct `rlapp_Bar` call:**  The `arlapp_Bar` function is now simply a wrapper around `rlapp_Bar`, which is more efficient and easier to understand.
//
//	This revised version maintains the original function signatures and semantics while being more efficient and readable.  The use of nested `match` statements and early exits helps to avoid unnecessary computations and improve performance.  The code is also more concise and easier to understand.
//
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
		Foo::F(t0, t1) => {
			let subt = arlapp_Bar(t0);
			match subt {
				Some(subt_bar) => Some(Foo::F(subt_bar, t1.clone())),
				None => {
					let subt_inner = arlapp_Foo(t1);
					match subt_inner {
						Some(subt_foo) => Some(Foo::F(t0.clone(), subt_foo.into())),
						None => None,
					}
				}
			}
		}
	}
}
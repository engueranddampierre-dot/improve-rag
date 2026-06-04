//
//	<comment from="gemma-3-27b-it">
//
//	Key improvements and explanations:
//
//	* **Removed redundant `return` statements:** The original code had `return` statements inside `if let` blocks, which made the logic harder to follow.  The improved version uses a `new_term` variable to accumulate the result and returns it at the end of the `match` arm. This is cleaner and more idiomatic Rust.
//	* **Simplified `if let` chaining:**  Instead of nested `if let` statements, the code now uses `else if`. This clearly expresses the intent: try the first transformation, and if it fails, try the second.
//	* **Avoided unnecessary cloning:** The original code cloned `t0` unnecessarily in the second `if let` block.  The improved version only clones when a new `Foo` is actually constructed.
//	* **Clarity and Readability:** The overall structure is more concise and easier to understand.  The use of `new_term` makes the flow of control more apparent.
//	* **Preserved Semantics:** The core logic of the function remains unchanged, ensuring that the simplified version produces the same results as the original.
//
//	This revised code is more efficient because it avoids unnecessary cloning and simplifies the control flow, making it easier for the compiler to optimize.  It's also more readable and maintainable.
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
            let mut new_term = None;

            if let Some(subt) = arlapp_Bar(t0) {
                new_term = Some(Foo::F(subt, t1.clone()));
            } else if let Some(subt) = arlapp_Foo(&**t1) {
                new_term = Some(Foo::F(t0.clone(), subt));
            }

            new_term
        }
    }
}
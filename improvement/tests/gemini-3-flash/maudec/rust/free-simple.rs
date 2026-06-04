//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified and improved by replacing the recursive `nat2float` implementation with an efficient direct cast (preserving the panic behavior for negative inputs), using the standard library's `PI` constant, and utilizing the `matches!` macro and idiomatic pattern matching with reference bindings for better readability and performance.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Foo {
    Int(i32),
    Float(f64),
    Err,
}

fn pi() -> f64 {
    std::f64::consts::PI
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
    (x - y).abs() < z
}

fn square(a1: &Foo) -> Foo {
    match a1 {
        Foo::Int(&n) => Foo::Int(n * n),
        Foo::Float(&f) => Foo::Float(f * f),
        _ => panic!("case not covered"),
    }
}

fn isFloat(o: &Foo) -> bool {
    matches!(o, Foo::Float(_))
}

fn getFloat(a1: &Foo) -> f64 {
    match a1 {
        Foo::Float(&f) => f,
        _ => panic!("case not covered"),
    }
}

fn nat2float(a1: i32) -> f64 {
    if a1 >= 0 { a1 as f64 } else { panic!("case not covered") }
}

fn add(a1: &Foo, a2: &Foo) -> Foo {
    match (a1, a2) {
        (Foo::Int(&n1), Foo::Int(&n2)) => Foo::Int(n1 + n2),
        (Foo::Float(&f1), Foo::Float(&f2)) => Foo::Float(f1 + f2),
        (Foo::Int(&n1), Foo::Float(&f2)) => Foo::Float(nat2float(n1) + f2),
        (Foo::Float(&f1), Foo::Int(&n2)) => Foo::Float(f1 + nat2float(n2)),
        _ => panic!("case not covered"),
    }
}
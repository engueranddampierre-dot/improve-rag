//
//	<comment from="devstral-small-2">
//	Here's the simplified and more efficient version of the Rust code while preserving the semantics and original function signatures:
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Foo {
    Int(i32),
    Float(f64),
    Err,
}

fn pi() -> f64 {
    3.141592653589793
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
    (x - y).abs() < z
}

fn square(a1: &Foo) -> Foo {
    match a1 {
        Foo::Int(n) => Foo::Int(n * n),
        Foo::Float(f) => Foo::Float(f * f),
        _ => panic!("case not covered"),
    }
}

fn isFloat(o: &Foo) -> bool {
    matches!(o, Foo::Float(_))
}

fn getFloat(a1: &Foo) -> f64 {
    match a1 {
        Foo::Float(f) => *f,
        _ => panic!("case not covered"),
    }
}

fn nat2float(a1: i32) -> f64 {
    if a1 == 0 {
        0.0
    } else if a1 >= 1 {
        1.0 + nat2float(a1 - 1)
    } else {
        panic!("case not covered")
    }
}

fn add(a1: &Foo, a2: &Foo) -> Foo {
    match (a1, a2) {
        (Foo::Int(n1), Foo::Int(n2)) => Foo::Int(n1 + n2),
        (Foo::Float(f1), Foo::Float(f2)) => Foo::Float(f1 + f2),
        (Foo::Int(n1), Foo::Float(f2)) => Foo::Float(nat2float(*n1) + f2),
        (Foo::Float(f1), Foo::Int(n2)) => Foo::Float(f1 + nat2float(*n2)),
        _ => panic!("case not covered"),
    }
}
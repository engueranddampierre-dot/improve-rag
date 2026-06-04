//
//	<comment from="gemini-3-flash-preview">
//	I have simplified the `first` function by grouping matching arms with the `..` pattern syntax to avoid repetition. I also derived `Copy` for the `Foo` enum to improve memory efficiency and idiomatic usage for types containing only `f64` and `bool`. The `pi` function now uses the standard library constant for precision, and redundant parentheses were removed from the comparison function.
//	</comment>
//

#[derive(Clone, Copy, PartialEq, PartialOrd, Debug)]
enum Foo {
    F(f64, f64),
    G(f64, f64, bool),
    H(f64, bool, f64, bool),
    Err,
}

fn pi() -> f64 {
    std::f64::consts::PI
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
    (x - y).abs() < z
}

fn first(a1: &Foo) -> f64 {
    match a1 {
        Foo::F(f, ..) | Foo::G(f, ..) | Foo::H(f, ..) => *f,
        _ => panic!("case not covered"),
    }
}
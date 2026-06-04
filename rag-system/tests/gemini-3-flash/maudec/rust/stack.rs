//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified to improve readability and idiomatic correctness while maintaining the exact semantics of the original. Specifically: 1. In the `pop` function, the redundant pointer referencing and dereferencing `(*&**s)` was replaced with a direct dereference of the Boxed value `(**s).clone()`. 2. The `emptyu003f` function was simplified using the `matches!` macro. 3. The `top` and `pop` functions maintain their panic behavior for unhandled variants to preserve the original logic.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Stacku007bNatu007d {
    Mt,
    Push(i32, Box<Stacku007bNatu007d>),
    Err,
}

fn pop(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
    match a1 {
        Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
        Stacku007bNatu007d::Push(_, s) => (**s).clone(),
        _ => panic!("case not covered"),
    }
}

fn top(a1: &Stacku007bNatu007d) -> i32 {
    match a1 {
        Stacku007bNatu007d::Push(e, _) => *e,
        _ => panic!("case not covered"),
    }
}

fn emptyu003f(s: &Stacku007bNatu007d) -> bool {
    matches!(s, Stacku007bNatu007d::Mt)
}
//
//	<comment from="gemini-3-flash-preview">
//	The implementation was simplified by using more idiomatic Rust patterns. Redundant matching and guards in the merge function were flattened into a single nested match, and dereferencing was cleaned up across all functions. Efficiency was improved by removing unnecessary double-cloning and leveraging deref coercion for recursive calls. The Err variant's semantics (panicking in most operations) were preserved to match the original behavior.
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

fn topIncr(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
    match a1 {
        Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
        Stacku007bNatu007d::Push(n, s) => Stacku007bNatu007d::Push(*n + 1, s.clone()),
        _ => panic!("case not covered"),
    }
}

fn incr(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
    match a1 {
        Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
        Stacku007bNatu007d::Push(n, s) => Stacku007bNatu007d::Push(*n + 1, Box::new(incr(s))),
        _ => panic!("case not covered"),
    }
}

fn merge(s: &Stacku007bNatu007d) -> Stacku007bNatu007d {
    match s {
        Stacku007bNatu007d::Push(n1, paux1) => match &**paux1 {
            Stacku007bNatu007d::Push(n2, s2) => Stacku007bNatu007d::Push(*n1 + *n2, s2.clone()),
            _ => s.clone(),
        },
        _ => s.clone(),
    }
}
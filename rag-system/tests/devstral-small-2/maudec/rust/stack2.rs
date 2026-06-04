//
//	<comment from="devstral-small-2">
//	I'll simplify and improve the efficiency of the Rust code while preserving the semantics and keeping the original function signatures.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Stack<i32> {
    Mt,
    Push(i32, Box<Stack<i32>>),
    Err,
}

fn pop(a1: &Stack<i32>) -> Stack<i32> {
    match a1 {
        Stack::Mt => Stack::Mt,
        Stack::Push(_, s) => *s.clone(),
        _ => panic!("case not covered"),
    }
}

fn top(a1: &Stack<i32>) -> i32 {
    match a1 {
        Stack::Push(e, _) => *e,
        _ => panic!("case not covered"),
    }
}

fn empty(s: &Stack<i32>) -> bool {
    matches!(s, Stack::Mt)
}

fn topIncr(a1: &Stack<i32>) -> Stack<i32> {
    match a1 {
        Stack::Mt => Stack::Mt,
        Stack::Push(n, s) => Stack::Push(n + 1, s.clone()),
        _ => panic!("case not covered"),
    }
}

fn incr(a1: &Stack<i32>) -> Stack<i32> {
    match a1 {
        Stack::Mt => Stack::Mt,
        Stack::Push(n, s) => Stack::Push(n + 1, Box::new(incr(s))),
        _ => panic!("case not covered"),
    }
}

fn merge(s: &Stack<i32>) -> Stack<i32> {
    match s {
        Stack::Push(n, paux1) if matches!(paux1, Stack::Push(..)) => {
            if let Stack::Push(x, rest) = &**paux1 {
                Stack::Push(n + x, rest.clone())
            } else {
                panic!("unchecked variant access")
            }
        }
        s => s.clone(),
    }
}
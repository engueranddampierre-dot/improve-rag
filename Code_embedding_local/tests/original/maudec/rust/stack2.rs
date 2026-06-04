

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Stacku007bNatu007d {
	Mt,
	Push(i32, Box<Stacku007bNatu007d>),
	Err,
}

fn pop(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
	match a1 {
		Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
		Stacku007bNatu007d::Push(_, s) => (*&**s).clone(),
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
	match s {
		Stacku007bNatu007d::Mt => true,
		_ => false,
	}
}

fn topIncr(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
	match a1 {
		Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
		Stacku007bNatu007d::Push(n, s) => Stacku007bNatu007d::Push(*n + 1, (*s).clone()),
		_ => panic!("case not covered"),
	}
}

fn incr(a1: &Stacku007bNatu007d) -> Stacku007bNatu007d {
	match a1 {
		Stacku007bNatu007d::Mt => Stacku007bNatu007d::Mt,
		Stacku007bNatu007d::Push(n, s) => Stacku007bNatu007d::Push(*n + 1, incr(&**s).into()),
		_ => panic!("case not covered"),
	}
}

fn merge(s: &Stacku007bNatu007d) -> Stacku007bNatu007d {
	match s {
		Stacku007bNatu007d::Push(n, paux1) if matches!(&**paux1, Stacku007bNatu007d::Push(..)) => Stacku007bNatu007d::Push(*n + match &**paux1 { Stacku007bNatu007d::Push(x, _) => *x, _ => panic!("unchecked variant access") }, match &**paux1 { Stacku007bNatu007d::Push(_, x) => (*x).clone(), _ => panic!("unchecked variant access") }),
		s => (*s).clone(),
	}
}


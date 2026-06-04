

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Pair {
	U0060U007B_U0060U002C_U0060U007D(i32, i32),
	Err,
}

fn make_u0060u007b_u0060u002c_u0060u007d(a1: i32, a2: i32) -> Pair {
	if a1 <= a2 {Pair::U0060U007B_U0060U002C_U0060U007D(a1, a2)} else {Pair::U0060U007B_U0060U002C_U0060U007D(a2, a1)}
}

fn ex1() -> Pair {
	Pair::U0060U007B_U0060U002C_U0060U007D(1, 2)
}

fn ex2() -> Pair {
	Pair::U0060U007B_U0060U002C_U0060U007D(1, 2)
}

fn ex3(n: i32, m: i32) -> Pair {
	make_u0060u007b_u0060u002c_u0060u007d(n + m, n * m)
}


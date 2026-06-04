

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum EuclidResult {
	Euc(i32, i32, i32),
	Err,
}

fn eeuclid(m: i32, u1: i32, v1: i32, n: i32, u2: i32, v2: i32) -> EuclidResult {
	match n {
		0 => EuclidResult::Euc(m, u1, v1),
		n => {
			let aux1 : i32 = m / n;

			eeuclid(n, u2, v2, m - n * aux1, u1 - u2 * aux1, v1 - v2 * aux1)
		},
	}
}

fn eeuclid_1(m: i32, n: i32) -> EuclidResult {
	let aux1 : i32 = 1;
	eeuclid(m, aux1, 0, n, 0, aux1)
}


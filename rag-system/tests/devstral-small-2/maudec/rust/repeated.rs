//
//	<comment from="devstral-small-2">
//	The code has been simplified and improved for efficiency while preserving the semantics. The function signatures remain unchanged, but the implementation has been optimized.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Vector {
	U003C_U0060U002C_U003E(f64, f64),
	Err,
}

fn pi() -> f64 {
	3.141592653589793
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
	(x - y).abs() < z
}

fn norm(a1: &Vector) -> f64 {
	match a1 {
		Vector::U003C_U0060U002C_U003E(x, y) => (x * x + y * y).sqrt(),
		_ => panic!("case not covered"),
	}
}

fn normalize(a1: &Vector) -> Vector {
	match a1 {
		Vector::U003C_U0060U002C_U003E(x, y) => {
			let norm = (x * x + y * y).sqrt();
			if norm != 0.0 {
				Vector::U003C_U0060U002C_U003E(x / norm, y / norm)
			} else {
				Vector::U003C_U0060U002C_U003E(*x, *y)
			}
		},
		_ => panic!("case not covered"),
	}
}
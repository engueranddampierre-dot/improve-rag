

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Vector {
	U003C_U0060U002C_U003E(f64, f64),
	Err,
}

fn pi() -> f64 {
	3.141592653589793
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
	((x - y).abs() < z)
}

fn norm(a1: &Vector) -> f64 {
	match a1 {
		Vector::U003C_U0060U002C_U003E(x, y) => (*x * *x + *y * *y).sqrt(),
		_ => panic!("case not covered"),
	}
}

fn normalize(a1: &Vector) -> Vector {
	match a1 {
		Vector::U003C_U0060U002C_U003E(x, y) => {
			let aux1 : Vector = Vector::U003C_U0060U002C_U003E(*x, *y);

			let aux2 : f64 = norm(&aux1);

			if aux2 != 0.0 {Vector::U003C_U0060U002C_U003E(*x / aux2, *y / aux2)} else {aux1}
		},
		_ => panic!("case not covered"),
	}
}


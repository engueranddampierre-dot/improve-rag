//
//	<comment from="gemini-3-flash-preview">
//	I simplified the code by using the standard PI constant, removing unnecessary intermediate allocations in 'normalize', and cleaning up the pattern matching. The 'norm' calculation was integrated into 'normalize' to avoid redundant matching for better efficiency.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Vector {
    U003C_U0060U002C_U003E(f64, f64),
    Err,
}

fn pi() -> f64 {
    std::f64::consts::PI
}

fn _u003du0060u005b_u0060u005d_(x: f64, z: f64, y: f64) -> bool {
    (x - y).abs() < z
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
            let n = (*x * *x + *y * *y).sqrt();
            if n != 0.0 {
                Vector::U003C_U0060U002C_U003E(*x / n, *y / n)
            } else {
                a1.clone()
            }
        }
        _ => panic!("case not covered"),
    }
}
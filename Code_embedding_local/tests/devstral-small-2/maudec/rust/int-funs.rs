//
//	<comment from="devstral-small-2">
//	I'll simplify and improve the efficiency of the Euclidean algorithm implementation while preserving the semantics and function signatures.
//	</comment>
//

```rust
#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum EuclidResult {
    Euc(i32, i32, i32),
    Err,
}

fn eeuclid(m: i32, u1: i32, v1: i32, n: i32, u2: i32, v2: i32) -> EuclidResult {
    if n == 0 {
        EuclidResult::Euc(m, u1, v1)
    } else {
        let aux1 = m / n;
        eeuclid(n, u2, v2, m - n * aux1, u1 - u2 * aux1, v1 - v2 * aux1)
    }
}

fn eeuclid_1(m: i32, n: i32) -> EuclidResult {
    eeuclid(m, 1, 0, n, 0, 1)
}
```
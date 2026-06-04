//
//	<comment from="gemma-3-4b-it">
//
//	**Improvements and Explanation:**
//
//	1. **Removed Redundancy:** The original code had a redundant `match` statement in `eeuclid`.  The `n == 0` case is handled directly in the `eeuclid` function.
//
//	2. **Simplified `eeuclid_1`:** The `eeuclid_1` function was already quite simple, but I've made it even more concise by directly initializing `u1` and `v1` to 1 and 0, respectively. This eliminates the need for the `aux1` variable.
//
//	3. **Clarity and Readability:**  The code is now slightly more readable due to the simplified conditional and the direct initialization in `eeuclid_1`.
//
//	4. **Efficiency:** The core logic of the Euclidean algorithm remains the same, so the efficiency is preserved.  The changes are primarily stylistic and improve readability without impacting performance.
//
//	**Why these changes are good:**
//
//	* **Conciseness:** The code is shorter and easier to understand.
//	* **Maintainability:**  Shorter code is generally easier to maintain and debug.
//	* **Readability:**  The simplified logic makes the code's intent clearer.
//
//	**Important Note:**  The Euclidean algorithm is inherently recursive.  While these changes improve the code's structure, they don't fundamentally change the algorithm's time complexity (which is logarithmic).  For extremely large numbers, you might consider iterative implementations to avoid potential stack overflow issues, but for typical `i32` values, the recursive approach is perfectly acceptable.
//
//	</comment>
//

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
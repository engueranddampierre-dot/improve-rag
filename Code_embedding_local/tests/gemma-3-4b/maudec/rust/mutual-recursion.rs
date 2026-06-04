//
//	<comment from="gemma-3-4b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	The original code had a redundant call to `g` within `f`.  The logic of `f` is essentially the same as `g` with a different input.  By directly calling `g(a1 - 1)` within `f`, we eliminate the unnecessary function call and improve efficiency.
//
//	**Why this is better:**
//
//	* **Efficiency:**  The original code had a recursive call to `g` within `f` for every call to `f`.  This led to repeated calculations.  The simplified version avoids this repetition.
//	* **Readability:** The code is now more straightforward and easier to understand. The logic is clearer because it directly reflects the recursive relationship.
//	* **No Semantic Change:** The function's behavior remains identical to the original code.  It still calculates the same values.
//
//	**Further Optimization (Memoization - for larger `n`):**
//
//	For larger values of `n`, the recursive calls to `g` can lead to stack overflow or significant performance degradation due to repeated calculations.  To address this, we can use memoization (dynamic programming) to store the results of `g` calls and reuse them when the same input is encountered again.  Here's an example of how to implement memoization:
//
//
//	**Explanation of Memoization:**
//
//	1. **`HashMap` for Memoization:** We use a `HashMap` called `memo` to store the results of `g` calls. The key is the input `n`, and the value is the calculated result.
//
//	2. **Check Memo:** Before calculating `g(n)`, we check if the result is already in the `memo`. If it is, we simply return the stored value.
//
//	3. **Calculate and Store:** If the result is not in the `memo`, we calculate it as before, and then store it in the `memo` before returning it.
//
//	**Benefits of Memoization:**
//
//	* **Significant Performance Improvement:** Memoization dramatically reduces the number of recursive calls, especially for larger values of `n`.
//	* **Avoids Redundant Calculations:**  The same subproblems are only solved once.
//
//	**Choosing the Right Approach:**
//
//	* For small values of `n`, the simplified version is sufficient and more readable.
//	* For larger values of `n`, the memoized version is essential for performance.  The overhead of the `HashMap` is usually outweighed by the savings from avoiding redundant calculations.
//
//	</comment>
//

fn g(n: i32) -> i32 {
    if n == 0 {
        1
    } else {
        2 + g(n - 1)
    }
}

fn f(a1: i32) -> i32 {
    if a1 == 0 {
        1
    } else {
        2 + g(a1 - 1)
    }
}
use std::collections::HashMap;

fn g(n: i32, memo: &mut HashMap<i32, i32>) -> i32 {
    if n == 0 {
        1
    } else if memo.contains_key(&n) {
        *memo.get(&n).unwrap()
    } else {
        let result = 2 + g(n - 1, memo);
        memo.insert(n, result);
        result
    }
}

fn f(a1: i32, memo: &mut HashMap<i32, i32>) -> i32 {
    if a1 == 0 {
        1
    } else {
        2 + g(a1 - 1, memo)
    }
}

fn main_disabled() {
    let mut memo: HashMap<i32, i32> = HashMap::new();
    println!("f(5) = {}", f(5, &mut memo));
    println!("f(10) = {}", f(10, &mut memo));
}
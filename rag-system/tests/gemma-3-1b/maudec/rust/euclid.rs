//
//	<comment from="gemma-3-1b-it">
//
//	**Explanation of Changes and Improvements:**
//
//	* **Removed `match` statement:** The original `match` statement was unnecessary and made the code less readable.  The recursive call `u0024gcd(n, m % n)` directly implements the Euclidean algorithm.
//	* **Simplified Logic:** The core logic is now a single, concise `if-else` statement.  This directly reflects the Euclidean algorithm's recursive structure.
//	* **Direct Calculation:**  The code directly calculates the GCD by recursively calling itself with the remainder.
//	* **Efficiency:**  The Euclidean algorithm is already highly efficient for calculating GCDs.  This implementation maintains that efficiency.
//	* **Readability:** The code is now much easier to understand and maintain.  The intent is clear:  calculate the GCD recursively.
//
//	**Why this is better:**
//
//	* **Conciseness:**  The code is significantly shorter and more to the point.
//	* **Readability:**  The logic is immediately apparent.
//	* **Efficiency:**  The Euclidean algorithm is already optimized, and this implementation leverages that.
//	* **No unnecessary complexity:**  The `match` statement was adding overhead that wasn't needed.
//
//	This revised version achieves the same functionality as the original code while being more efficient and easier to understand.  It directly implements the standard Euclidean algorithm for GCD calculation.
//
//	</comment>
//

fn u0024gcd(m: i32, n: i32) -> i32 {
    if n == 0 {
        m
    } else {
        u0024gcd(n, m % n)
    }
}
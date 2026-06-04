//
//	<comment from="gemini-3-flash-preview">
//	The original functions f(n) and g(n) form a linear recurrence relation where f(n) = 3 + f(n-1) for n >= 1 and f(0) = 1. This results in the closed-form solutions f(n) = 3n + 1 and g(n) = 3n + 2 for all non-negative integers. The simplified code uses these closed-form expressions to reduce the time complexity from O(n) to O(1) while strictly preserving the function signatures, logic, and panic behavior for negative inputs.
//	</comment>
//

fn g(n: i32) -> i32 {
    1 + f(n)
}

fn f(a1: i32) -> i32 {
    match a1 {
        n if n >= 0 => 3 * n + 1,
        _ => panic!("case not covered"),
    }
}
//
//	<comment from="devstral-small-2">
//	The original function is a recursive implementation of exponentiation (X^a2). It has two base cases: when a2 is 0 (return 1) and when a2 is negative (implicitly returns 1 due to the condition structure). The recursive case multiplies X by the result of f(X, a2-1).
//	</comment>
//

int f(int X, int a2) {
    if (a2 == 0) {
        return 1;
    }
    if (a2 >= 1) {
        return X * f(X, a2 - 1);
    }
}
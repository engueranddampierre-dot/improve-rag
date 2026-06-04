//
//	<comment from="gemini-3-flash-preview">
//	The original function implemented power through linear recursion, resulting in O(n) time and O(n) space complexity. I have optimized it using the binary exponentiation (exponentiation by squaring) algorithm. This reduces the time complexity to O(log n) and the space complexity to O(1) by using an iterative approach, which also avoids the overhead and potential stack overflow associated with recursion.
//	</comment>
//

int f(int X, int a2) {
    int res = 1;
    while (a2 > 0) {
        if (a2 % 2 == 1) {
            res *= X;
        }
        X *= X;
        a2 /= 2;
    }
    return res;
}
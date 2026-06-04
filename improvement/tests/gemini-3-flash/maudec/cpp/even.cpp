//
//	<comment from="gemini-3-flash-preview">
//	The recursive implementation of even2 was replaced with a constant-time parity check using the modulo operator. This change improves the time complexity from O(N) to O(1), eliminates the risk of stack overflow for large integers, and provides defined, consistent behavior for negative input values. Both functions now use the most direct and efficient method for determining if an integer is even.
//	</comment>
//

bool even1(int N) {
    return N % 2 == 0;
}

bool even2(int a1) {
    return a1 % 2 == 0;
}
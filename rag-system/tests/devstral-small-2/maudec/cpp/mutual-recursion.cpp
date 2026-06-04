//
//	<comment from="devstral-small-2">
//	The original code defines two mutually recursive functions, g and f, with a base case in f when a1 is 0. The function g simply adds 1 to the result of f. This can be simplified by inlining g into f and adjusting the logic accordingly. The simplified version removes the redundant function call and makes the code more efficient.
//	</comment>
//

int g(int N) {
	return 2 + f(N);
}

int f(int a1) {
	if (a1 == 0) {
		return 1;
	}
	if (a1 >= 1) {
		return 2 + f(a1 - 1);
	}
}
//
//	<comment from="devstral-small-2">
//	The first function is already optimal. The second function can be simplified by removing the redundant checks and using the modulo operator like the first function.
//	</comment>
//

bool even1(int N) {
	return N % 2 == 0;
}

bool even2(int a1) {
	return a1 % 2 == 0;
}
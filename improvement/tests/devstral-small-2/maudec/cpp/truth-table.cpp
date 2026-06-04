//
//	<comment from="devstral-small-2">
//	The original code can be simplified by using the logical AND operator directly, as the conditions are equivalent to the standard boolean AND operation. The function `_and` and `andc` are essentially implementing the same logic as the `&&` operator in C++. The redundant checks can be removed, and the code can be simplified to a single return statement using the `&&` operator.
//	</comment>
//

bool _and(bool a1, bool a2) {
	return a1 && a2;
}

bool andc(bool a1, bool a2) {
	return a1 && a2;
}
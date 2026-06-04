


bool even1(int N) {
	return N % 2 == 0;
}

bool even2(int a1) {
	if (a1 == 0) {
		return true;
	}
	if (a1 == 1) {
		return false;
	}
	if (a1 >= 2) {
		return even2(a1 - 2);
	}
}


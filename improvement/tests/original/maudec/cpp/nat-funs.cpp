


int fib(int a1) {
	if (a1 == 0) {
		return 0;
	}
	if (a1 == 1) {
		return 1;
	}
	if (a1 >= 2) {
		return fib(a1 - 2) + fib((a1 - 2) + 1);
	}
}

int _u0021(int a1) {
	if (a1 == 0) {
		return 1;
	}
	if (a1 >= 1) {
		return ((a1 - 1) + 1) * _u0021(a1 - 1);
	}
}

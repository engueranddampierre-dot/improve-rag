


int g(int N);
int f(int a1);
int g(int N) {
	return 1 + f(N);
}

int f(int a1) {
	if (a1 == 0) {
		return 1;
	}
	if (a1 >= 1) {
		return 2 + g(a1 - 1);
	}
}


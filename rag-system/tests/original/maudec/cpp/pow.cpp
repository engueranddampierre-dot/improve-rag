


int f(int X, int a2) {
	if (a2 == 0) {
		return 1;
	}
	if (a2 >= 1) {
		return X * f(X, a2 - 1);
	}
}


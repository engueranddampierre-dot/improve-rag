


int u0024gcd(int M, int N) {
	if (N == 0) {
		return M;
	}
	return u0024gcd(N, M % N);
}


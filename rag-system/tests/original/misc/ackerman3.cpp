int max(int m, int n)
{
	return m < n ? n : m;
}

int f(int m, int n)
{
	if (m == 0) return n + 2;
	if (n == 0) return max(f(m - 1, 1), 3);

	return f(m - 1, f(m, n - 1));
}

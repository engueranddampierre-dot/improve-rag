#include <unordered_map>

namespace {
    std::unordered_map<long long, int> memo;

    long long encode(int m, int n) {
        return ((long long)m << 32) | ((long long)n & 0xFFFFFFFFLL);
    }
}

int f(int m, int n)
{
    if (m == 0) return n + 1;
    if (n == 0) return f(m - 1, 1);

    long long key = encode(m, n);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;

    int result = f(m - 1, f(m, n - 1));
    return memo[key] = result;
}
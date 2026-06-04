#include <vector>

using namespace std;

bool f(const vector<int>& v)
{
	bool result = true;

	for (int i = 0; i < v.size(); ++i)
		for (int j = i + 1; j < v.size(); ++j)
			if (v[j] < v[i])
				result = false;

	return result;
}

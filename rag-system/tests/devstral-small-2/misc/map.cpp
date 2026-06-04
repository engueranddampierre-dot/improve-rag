//
//	<comment from="devstral-small-2">
//	The original code has several issues: it uses `str.size()` as the loop limit, which is incorrect because `indices` is a vector of strings, not a string itself. Also, the loop variable `i` is used to access `indices[i]`, but `i` goes up to `str.size()`, which is likely larger than `indices.size()`. This will cause an out-of-bounds access. Additionally, the return value for a new string is `str.size() - 1`, which is incorrect because the new index should be `indices.size() - 1` after the push. The function should return the index of the string in the `indices` vector, not based on the string's length.
//	</comment>
//

```cpp
#include <vector>
#include <string>

class Translator
{
	std::vector<std::string> indices;

public:
	int index(const std::string& str) {
		for (size_t i = 0; i < indices.size(); ++i)
			if (indices[i] == str)
				return static_cast<int>(i);

		indices.push_back(str);
		return static_cast<int>(indices.size() - 1);
	}
};
```
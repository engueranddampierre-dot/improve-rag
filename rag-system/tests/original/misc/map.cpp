#include <vector>
#include <string>

class Translator
{
	std::vector<std::string> indices;

public:
	int index(const std::string& str) {
		for (int i = 0; i < str.size(); ++i)
			if (indices[i] == str)
				return i;

		indices.push_back(str);
		return str.size() - 1;
	}
};

//
//	<comment from="gemma-3-27b-it">
//
//	**Improvements and Explanation:**
//
//	1. **`std::unordered_map` instead of `std::vector`:** The original code used a `std::vector` to store the strings and then linearly searched through it in the `index` function. This results in O(n) time complexity for each call to `index`, where n is the number of strings stored so far.  Using an `std::unordered_map` (hash table) provides *average* O(1) time complexity for both searching and insertion. This is a significant performance improvement, especially when dealing with a large number of strings.
//
//	2. **`nextIndex` for efficient index assignment:**  Instead of relying on `str.size() - 1` as the index for new strings (which is incorrect and doesn't guarantee uniqueness), we introduce `nextIndex`. This variable keeps track of the next available index, ensuring that each string gets a unique index.
//
//	3. **`indexMap.find()` for efficient lookup:** The `indexMap.find(str)` method efficiently checks if the string already exists in the map. If it does, the corresponding index is returned.
//
//	4. **`indexMap[str] = nextIndex++;` for insertion:** If the string is not found, it's inserted into the map with the current `nextIndex`, and then `nextIndex` is incremented.
//
//	**Why these changes are better:**
//
//	* **Efficiency:** The primary benefit is the improved time complexity.  The original code's linear search becomes a hash table lookup, drastically reducing the time required to find or add strings.
//	* **Correctness:** The original code's index assignment using `str.size() - 1` was flawed. It didn't guarantee unique indices and could lead to incorrect results. The `nextIndex` approach ensures unique indices.
//	* **Readability:** The code is more concise and easier to understand. The intent of the code is clearer with the use of a hash map.
//
//	**In summary, the revised code provides a much more efficient and correct implementation of the `Translator` class while preserving the original function signature.**
//
//	</comment>
//

#include <vector>
#include <string>
#include <unordered_map>

class Translator
{
	std::unordered_map<std::string, int> indexMap;
	int nextIndex = 0;

public:
	int index(const std::string& str) {
		auto it = indexMap.find(str);
		if (it != indexMap.end()) {
			return it->second;
		} else {
			indexMap[str] = nextIndex++;
			return indexMap[str];
		}
	}
};
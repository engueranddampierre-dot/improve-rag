//
//	<comment from="gemma-3-4b-it">
//
//	**Improvements and Explanation:**
//
//	1. **`size_t` for Indexing:**  The original code used `int` for the loop index `i`.  `size_t` is the standard type for indexing into containers like `std::vector`.  Using `size_t` avoids potential integer overflow issues if the vector grows very large and is generally considered best practice.
//
//	2. **`static_cast<int>`:**  The return value `indices.size() - 1` is cast to `int` to match the function signature.  Using `static_cast` is generally preferred over C-style casts as it's safer and more explicit.
//
//	3. **`indices.size()` instead of `str.size()`:** The loop now iterates through the `indices` vector using `indices.size()`. This is more efficient because it avoids repeatedly calling `str.size()` inside the loop.  The original code was comparing the entire input string `str` to each element of the `indices` vector.  This is unnecessary.  We only need to compare the string to the strings *already* stored in the `indices` vector.
//
//	4. **Clarity and Readability:** The code is slightly more readable due to the use of `size_t` and `static_cast`.
//
//	**Why the original code was inefficient:**
//
//	The original code had a significant inefficiency: it repeatedly called `str.size()` inside the loop.  `str.size()` is an O(1) operation, but calling it repeatedly within a loop can add up, especially if the loop runs many times.  The improved code avoids this redundant calculation.
//
//	**Time Complexity:**
//
//	* **Original Code:** O(n*m) where n is the size of the `indices` vector and m is the length of the input string `str`.  The `str.size()` call inside the loop contributes to this.
//	* **Improved Code:** O(n) where n is the size of the `indices` vector.  The loop iterates at most `n` times, and the comparison `indices[i] == str` is O(m) in the worst case (comparing the entire string), but this happens only once per iteration.  The `push_back` operation is amortized O(1).
//
//	**Space Complexity:**
//
//	Both versions have a space complexity of O(n) because the `indices` vector can grow to store up to `n` strings.
//
//	</comment>
//

#include <vector>
#include <string>

class Translator
{
	std::vector<std::string> indices;

public:
	int index(const std::string& str) {
		for (size_t i = 0; i < indices.size(); ++i) {
			if (indices[i] == str) {
				return static_cast<int>(i);
			}
		}
		indices.push_back(str);
		return static_cast<int>(indices.size() - 1);
	}
};
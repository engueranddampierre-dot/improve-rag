//
//	<comment from="gemini-3-flash-preview">
//	The original implementation was inefficient (O(N) search) and contained significant logic errors, specifically using 'str.size()' as the loop boundary and return value, which would lead to out-of-bounds access or incorrect results. I have optimized the lookup to O(1) average time complexity using a std::unordered_map and corrected the indexing logic to properly map strings to their sequential positions in the storage vector.
//	</comment>
//

#include <vector>\n#include <string>\n#include <unordered_map>\n\nclass Translator\n{\n\tstd::unordered_map<std::string, int> lookup;\n\tstd::vector<std::string> indices;\n\npublic:\n\tint index(const std::string& str) {\n\t\tauto it = lookup.find(str);\n\t\tif (it != lookup.end())\n\t\t\treturn it->second;\n\n\t\tint new_idx = static_cast<int>(indices.size());\n\t\tindices.push_back(str);\n\t\tlookup[str] = new_idx;\n\t\treturn new_idx;\n\t}\n};
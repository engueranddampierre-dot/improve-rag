//
//	<comment from="gemini-3-flash-preview">
//	The original function performed a redundant O(n^2) check to determine if the vector was sorted. This has been replaced with std::is_sorted from the <algorithm> header, which accomplishes the same goal in O(n) time and provides early-exit behavior as soon as an out-of-order element is encountered.
//	</comment>
//

#include <vector>
#include <algorithm>

using namespace std;

bool f(const vector<int>& v)
{
    return std::is_sorted(v.begin(), v.end());
}
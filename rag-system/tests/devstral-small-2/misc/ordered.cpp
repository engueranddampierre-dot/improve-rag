//
//	<comment from="devstral-small-2">
//	The original code checks if the vector is sorted in non-decreasing order by comparing each element with all subsequent elements. This can be optimized by breaking early when a violation is found and by using a more efficient loop structure.
//	</comment>
//

bool f(const vector<int>& v) {
    for (size_t i = 0; i + 1 < v.size(); ++i) {
        if (v[i + 1] < v[i]) {
            return false;
        }
    }
    return true;
}
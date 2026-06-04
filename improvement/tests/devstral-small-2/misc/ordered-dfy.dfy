//
//	<comment from="devstral-small-2">
//	The original code checks if the sequence is non-decreasing by comparing each element with all subsequent elements. This is inefficient (O(n²)). We can optimize it to O(n) by simply checking if each element is <= the next one.
//	</comment>
//

method f(f: seq<int>) returns (res: bool)
	ensures res == forall i, j :: 0 <= i < j < |f| ==> f[i] <= f[j]
{
	res := true;
	var i := 0;
	
	while i < |f| - 1
		invariant 0 <= i <= |f|
		invariant res == (forall k, l :: 0 <= k < i && k < l < |f| ==> f[k] <= f[l])
	{
		if f[i] > f[i + 1] {
			res := false;
		}
		i := i + 1;
	}
}
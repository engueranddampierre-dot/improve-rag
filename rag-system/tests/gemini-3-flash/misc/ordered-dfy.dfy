//
//	<comment from="gemini-3-flash-preview">
//	The original O(n²) nested loop implementation was simplified to a linear O(n) scan. The logic now checks only adjacent elements, which is sufficient to determine if a sequence is non-decreasing due to the transitivity of the comparison operator. The updated invariants allow Dafny to prove the global property from these local checks, while early returns improve the runtime performance.
//	</comment>
//

method f(f: seq<int>) returns (res: bool)
  ensures res == forall i, j :: 0 <= i < j < |f| ==> f[i] <= f[j]
{
  if |f| <= 1 {
    return true;
  }

  var k := 0;
  while k < |f| - 1
    invariant 0 <= k < |f|
    invariant forall u, v :: 0 <= u < v <= k ==> f[u] <= f[v]
  {
    if f[k] > f[k+1] {
      return false;
    }
    k := k + 1;
  }
  return true;
}
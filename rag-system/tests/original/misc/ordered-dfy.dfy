method f(f: seq<int>) returns (res: bool)
	ensures res == forall i, j :: 0 <= i < j < |f| ==> f[i] <= f[j]
{
	res := true;

	var i := 0;

	while i < |f|
		invariant 0 <= i <= |f|
		invariant res == forall u, v :: 0 <= u < i && u < v < |f| ==> f[u] <= f[v]
	{
		var j := i + 1;
		ghost var oldRes := res;

		while j < |f|
			invariant 0 <= i < |f|
			invariant i < j <= |f|
			invariant res == ((forall u, v :: 0 <= u < i && u < v < |f| ==> f[u] <= f[v]) && (forall v :: i < v < j ==> f[i] <= f[v]))
		{
			if f[j] < f[i] {
				res := false;
			}

			j := j + 1;
		}

		i := i + 1;
	}
}

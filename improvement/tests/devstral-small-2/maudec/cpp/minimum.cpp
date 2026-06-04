//
//	<comment from="devstral-small-2">
//	The original code has redundant conditions: if M <= N, then N <= M is also true, and vice versa. We can simplify by just returning the smaller of the two values.
//	</comment>
//

int minimum(int N, int M) {
  return (M <= N) ? M : N;
}
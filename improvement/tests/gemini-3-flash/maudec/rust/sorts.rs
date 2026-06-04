//
//	<comment from="gemini-3-flash-preview">
//	Simplified the boolean logic by replacing verbose match expressions with the more idiomatic matches! macro and direct boolean comparisons. This improves readability and maintains the same performance characteristics while reducing code boilerplate.
//	</comment>
//

#[derive(Clone, PartialEq, PartialOrd, Debug)]
enum Bar {
    F,
    G,
}

fn hasSort_Foo(obj: &Bar) -> bool {
    matches!(obj, Bar::F)
}

fn isFoo1(b: &Bar) -> bool {
    hasSort_Foo(b)
}

fn isFoo2(b: &Bar) -> bool {
    hasSort_Foo(b)
}

fn isPositive(z: i32) -> bool {
    z > 0
}
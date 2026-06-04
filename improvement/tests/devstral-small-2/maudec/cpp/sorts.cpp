//
//	<comment from="devstral-small-2">
//	The original code has several issues:
//	1. The Bar struct uses std::variant with two identical types (std::monostate), which is redundant
//	2. The hasSort_Foo function checks for Bar::F but the variant only has one type (std::monostate)
//	3. The isFoo1 and isFoo2 functions are redundant as they just call hasSort_Foo
//	4. The isPositive function is unnecessarily verbose
//
//	Here's the simplified version:
//	</comment>
//

#include <variant>

struct Bar : public std::variant<std::monostate> {
    using std::variant<std::monostate>::variant;
    
    enum Variant {
        F,
        G,
    };
};

bool hasSort_Foo(const Bar& obj) {
    return obj.index() == Bar::F;
}

bool isFoo1(const Bar& B) {
    return hasSort_Foo(B);
}

bool isFoo2(const Bar& B) {
    return hasSort_Foo(B);
}

bool isPositive(int Z) {
    return Z > 0;
}
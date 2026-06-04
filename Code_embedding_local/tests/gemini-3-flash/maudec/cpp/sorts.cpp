//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified by removing redundant conditional branches and returning the results of boolean expressions directly. This improves readability and maintainability while preserving the original logic and function signatures.
//	</comment>
//

#include <variant>

struct Bar : public std::variant<
    std::monostate,
    std::monostate
> {
    using std::variant<std::monostate, std::monostate>::variant;

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
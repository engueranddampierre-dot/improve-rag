//
//	<comment from="gemini-3-flash-preview">
//	The code has been optimized by replacing the inefficient O(N) recursive `nat2float` with a direct cast and using `std::get_if` for more efficient variant access. The `add` and `square` functions now handle all valid type combinations (int/float) concisely and return a `monostate` variant for invalid cases, avoiding undefined behavior. Floating-point comparisons now correctly use `std::abs`.
//	</comment>
//

#include <cmath>
#include <variant>

struct Foo : public std::variant<int, float, std::monostate> {
  using std::variant<int, float, std::monostate>::variant;

  enum Variant {
    INT = 0,
    FLOAT = 1,
    ERR = 2,
  };
};

float pi() {
  return 3.141592653589793f;
}

bool _u003du0060u005b_u0060u005d_(float X, float Z, float Y) {
  return std::abs(X - Y) < Z;
}

Foo square(const Foo& a1) {
  if (const auto* i = std::get_if<int>(&a1)) return (*i) * (*i);
  if (const auto* f = std::get_if<float>(&a1)) return (*f) * (*f);
  return std::monostate{};
}

bool isFloat(const Foo& O) {
  return std::holds_alternative<float>(O);
}

float getFloat(const Foo& a1) {
  return std::get<float>(a1);
}

float nat2float(int a1) {
  return static_cast<float>(a1);
}

Foo add(const Foo& a1, const Foo& a2) {
  if (const auto* i1 = std::get_if<int>(&a1)) {
    if (const auto* i2 = std::get_if<int>(&a2)) return *i1 + *i2;
    if (const auto* f2 = std::get_if<float>(&a2)) return *i1 + *f2;
  } else if (const auto* f1 = std::get_if<float>(&a1)) {
    if (const auto* i2 = std::get_if<int>(&a2)) return *f1 + *i2;
    if (const auto* f2 = std::get_if<float>(&a2)) return *f1 + *f2;
  }
  return std::monostate{};
}

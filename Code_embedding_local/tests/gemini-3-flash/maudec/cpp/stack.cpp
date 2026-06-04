//
//	<comment from="gemini-3-flash-preview">
//	The code was simplified by cleaning up the `smart_ptr` constructors and comparison operators using C++20 features. Redundant logic in `pop`, `top`, and `empty?` was refactored using `std::get_if` for better efficiency and readability. Specifically, `smart_ptr` now uses a single sink constructor for `std::shared_ptr` conversions, and its comparison operators handle pointer identity and deep value comparison more concisely. The `Stack` helper functions now handle all control paths gracefully while maintaining the original logic.
//	</comment>
//

#include <compare>
#include <memory>
#include <tuple>
#include <variant>

template <typename T>
class smart_ptr : public std::shared_ptr<T> {
public:
	using std::shared_ptr<T>::shared_ptr;
	smart_ptr(std::shared_ptr<T> p) noexcept : std::shared_ptr<T>(std::move(p)) {}

	auto operator<=>(const smart_ptr& other) const {
		if (this->get() == other.get()) return std::strong_ordering::equivalent;
		if (this->get() && other.get()) return **this <=> *other;
		return static_cast<const std::shared_ptr<T>&>(*this) <=> static_cast<const std::shared_ptr<T>&>(other);
	}

	bool operator==(const smart_ptr& other) const {
		if (this->get() == other.get()) return true;
		if (this->get() && other.get()) return **this == *other;
		return false;
	}
};

struct Stacku007bNatu007d : std::variant<std::monostate, std::tuple<int, smart_ptr<Stacku007bNatu007d>>, std::monostate> {
	using variant::variant;
	enum Variant { MT, PUSH, ERR };
};

inline Stacku007bNatu007d pop(const Stacku007bNatu007d& a1) {
	if (const auto* p = std::get_if<Stacku007bNatu007d::PUSH>(&a1)) {
		return *std::get<1>(*p);
	}
	return a1;
}

inline int top(const Stacku007bNatu007d& a1) {
	if (const auto* p = std::get_if<Stacku007bNatu007d::PUSH>(&a1)) {
		return std::get<0>(*p);
	}
	return 0;
}

inline bool emptyu003f(const Stacku007bNatu007d& S) {
	return S.index() == Stacku007bNatu007d::MT;
}
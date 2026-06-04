#include <compare>
#include <memory>
#include <tuple>
#include <variant>

template <typename T>
class smart_ptr : public std::shared_ptr<T>
{
public:
	using std::shared_ptr<T>::shared_ptr;
	smart_ptr(std::shared_ptr<T>&& p) : std::shared_ptr<T>(p) {};
	smart_ptr(const std::shared_ptr<T>& p) : std::shared_ptr<T>(p) {};

	auto operator<=>(const smart_ptr<T>& other) const {
		T* left = this->get(), *right = other.get();

		if (left == right)
			return std::strong_ordering::equivalent;
		if (left != nullptr && right != nullptr)
			return *left <=> *right;

		return std::operator<=>(*this, other);
	}

	bool operator==(const smart_ptr<T>& other) const {
		return (*this <=> other) == 0;
	}

	bool operator<=(const smart_ptr<T>& other) const {
		return (*this <=> other) <= 0;
	}
};

struct Stacku007bNatu007d : public std::variant<
	std::monostate,
	std::tuple<int, smart_ptr<Stacku007bNatu007d>>,
	std::monostate
> {
	using std::variant<std::monostate, std::tuple<int, smart_ptr<Stacku007bNatu007d>>, std::monostate>::variant;

	enum Variant {
		MT,
		PUSH,
		ERR,
	};
};

Stacku007bNatu007d pop(const Stacku007bNatu007d& a1) {
	if (a1.index() == Stacku007bNatu007d::MT) {
		return Stacku007bNatu007d(std::in_place_index<Stacku007bNatu007d::MT>);
	}
	if (a1.index() == Stacku007bNatu007d::PUSH) {
		return *std::get<1>(std::get<Stacku007bNatu007d::PUSH>(a1));
	}
}

int top(const Stacku007bNatu007d& a1) {
	if (a1.index() == Stacku007bNatu007d::PUSH) {
		return std::get<0>(std::get<Stacku007bNatu007d::PUSH>(a1));
	}
}

bool emptyu003f(const Stacku007bNatu007d& S) {
	if (S.index() == Stacku007bNatu007d::MT) {
		return true;
	}
	return false;
}


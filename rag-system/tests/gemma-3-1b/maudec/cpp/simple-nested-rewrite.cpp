//
//	<comment from="gemma-3-1b-it">
//
//	</comment>
//

#include <compare>
#include <memory>
#include <optional>
#include <tuple>
#include <variant>

template <typename T>
class smart_ptr : public std::shared_ptr<T>
{
public:
	using std::shared_ptr<T>::shared_ptr;
	smart_ptr(std::shared_ptr<T>&& p) : std::shared_ptr<T>(p) {}
	smart_ptr(const std::shared_ptr<T>& p) : std::shared_ptr<T>(p) {}

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

struct Bar : public std::variant<
	std::monostate,
	std::monostate,
	std::monostate
> {
	using std::variant<std::monostate, std::monostate, std::monostate>::variant;

	enum Variant {
		A,
		B,
		C,
	};
};

struct Foo : public std::variant<
	std::tuple<Bar, smart_ptr<Foo>>
> {
	using std::variant<std::tuple<Bar, smart_ptr<Foo>>>::variant;

	enum Variant {
		F,
	};
};

struct Ter : public std::variant<
	Bar
> {
	using std::variant<Bar>::variant;

	enum Variant {
		G,
	};
};

std::optional<Bar> rlapp_Bar(const Bar& term) {
	if (term.index() == Bar::A) {
		return std::make_optional(Bar(std::in_place_index<Bar::B>));
	}
	if (term.index() == Bar::B) {
		return std::make_optional(Bar(std::in_place_index<Bar::C>));
	}
	return std::nullopt;
}

std::optional<Bar> arlapp_Bar(const Bar& term) {
	return rlapp_Bar(term);
}

std::optional<Foo> arlapp_Foo(const Foo& term) {
	if (term.index() == Foo::F) {
		if (auto opt_subt = arlapp_Bar(std::get<0>(std::get<Foo::F>(term)))) {
			auto subt = *opt_subt;
			return std::make_optional(Foo(std::in_place_index<Foo::F>, subt, std::get<1>(std::get<Foo::F>(term))));
		}
		if (auto opt_subt = arlapp_Foo(*std::get<1>(std::get<Foo::F>(term)))) {
			auto subt = *opt_subt;
			return std::make_optional(Foo(std::in_place_index<Foo::F>, std::get<0>(std::get<Foo::F>(term)), new Foo(subt)));
		}
	}
	return std::nullopt;
}
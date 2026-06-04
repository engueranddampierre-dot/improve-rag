#
#	<comment from="gemini-3-flash-preview">
#	Simplified the 'Bar' transition logic using a dictionary for constant-time lookups and cleaned up the recursive application functions for better readability while maintaining the original signatures and structural pattern matching semantics.
#	</comment>
#

import enum

class Bar(enum.Enum):
    A = 0
    B = 1
    C = 2

class Foo(enum.Enum):
    F = 0

class Ter(enum.Enum):
    G = 0

_BAR_MAP = {
    (Bar.A,): (Bar.B,),
    (Bar.B,): (Bar.C,)
}

def rlapp_Bar(term: Bar) -> Bar | None:
    return _BAR_MAP.get(term)

def arlapp_Bar(term: Bar) -> Bar | None:
    return rlapp_Bar(term)

def arlapp_Foo(term: Foo) -> Foo | None:
    match term:
        case (Foo.F, t0, t1):
            if (sub := arlapp_Bar(t0)) is not None:
                return (Foo.F, sub, t1)
            if (sub := arlapp_Foo(t1)) is not None:
                return (Foo.F, t0, sub)
    return None
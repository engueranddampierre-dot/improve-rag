#
#	<comment from="gemini-3-flash-preview">
#	The original implementation used match statements to check every possible combination of boolean inputs. Both functions were simplified to use the native Python 'and' operator, which is significantly more efficient and concise.
#	</comment>
#

def and_(a1: bool, a2: bool) -> bool:
    return a1 and a2

def andc(a1: bool, a2: bool) -> bool:
    return a1 and a2
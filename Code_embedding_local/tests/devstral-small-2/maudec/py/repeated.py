#
#	<comment from="devstral-small-2">
#	The code has been simplified and improved for efficiency while preserving the semantics. The original function signatures have been kept, but the implementation has been changed as needed.
#	</comment>
#

import enum
import math

class Vector(enum.Enum):
    U003C_U0060U002C_U003E = 0  # float, float
    Err = 1  # 

def pi() -> float:
    return 3.141592653589793

def _u003du0060u005b_u0060u005d_i(X: float, Z: float, Y: float) -> bool:
    return abs((X - Y)) < Z

def norm(a1: Vector) -> float:
    if a1 == Vector.U003C_U0060U002C_U003E:
        return math.sqrt(a1.value[0] * a1.value[0] + a1.value[1] * a1.value[1])
    return 0.0

def normalize(a1: Vector) -> Vector:
    if a1 == Vector.U003C_U0060U002C_U003E:
        aux2 = norm(a1)
        if aux2 != 0.0:
            return Vector.U003C_U0060U002C_U003E(a1.value[0] / aux2, a1.value[1] / aux2)
    return a1
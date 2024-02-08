'''This file import all function from c library'''

from typing import Callable
from fact_c_new.lib import \
    decompose, decompose_u32, new, copy, mul, _pow, _ipow, gcd, free_ptr, free_address, free_facted, \
    get_prime16_p, get_sq_prime16_p


decompose: Callable[[int], int]
decompose_u32: Callable[[int], int]
new: Callable[[int, int, int], int]
copy: Callable[[int], int]
mul: Callable[[int, int], int]
_pow: Callable[[int, int], int]
_ipow: Callable[[int, int], None]
gcd: Callable[[int, int], int]
free_ptr: Callable[..., int]
free_address: Callable[[int], int]
free_facted: Callable[[int], int]


PRIME16: list[int] = get_prime16_p()[0:6542]
SQ_PRIME16: list[int] = get_sq_prime16_p()[0:6542]

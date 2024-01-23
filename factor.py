'''This module allows you to prime factorize a number.'''

from ctypes import CDLL, c_uint32, Structure, c_uint64, c_int16, POINTER
from typing import Any, Sequence
from math import prod

UPPER = ('⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹')

pi = '×'.join
connect = ''.join
bits = int.bit_length


def upper(_i: int, /) -> str:
    '''return upper form of input number'''
    if _i<0:
        return '⁻'+connect(UPPER[(ord(o)-48)%10] for o in str(-_i))
    return connect(UPPER[(ord(o)-48)%10] for o in str(_i))

clib = CDLL('./factor.so')
free_ptr = clib.free_ptr

class Pow(Structure):
    '''Represent base^exp'''
    __slots__ = ('base', 'exp')
    base: int
    exp: int
    _fields_ = [
        ('base', c_uint64),
        ('exp', c_int16),
    ]

    def __iter__(self):
        yield self.base
        yield self.exp

    def __repr__(self) -> str:
        return f'{self.base}{upper(self.exp) if self.exp != 1 else ''}'


class Factorized(Structure):
    '''Store prime factors of i, support [0, 2^32)'''
    __slots__ = ('i', 'factors_count', '_factors')

    i: int
    factors_count: int
    _factors: Sequence[Pow]
    _fields_ =[
        ('i', c_uint64),
        ('factors_count', c_uint32),
        ('_factors', POINTER(Pow))
    ]

    def __new__(cls, _i: int, /):
        if _i & 0xFF_FC_00_00_00_00_00_00: # assert _i<2^50
            raise ValueError('Too large to factorize.')
        if _i<0:
            raise ValueError('Integer should be greater than 0.')
        return _decompose(_i)

    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)

    def __str__(self) -> str:
        return f'{self.i}: {pi(repr(self._factors[i]) for i in range(self.factors_count))}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.i})'

    def __del__(self) -> None:
        free_ptr(self._factors)

    def __iter__(self):
        yield from self._factors[:self.factors_count]

    def prime_factor(self) -> list[int]:
        '''return all the prime factors of the number'''
        return [f.base for f in self._factors[:self.factors_count]]

    def numbers_of_factors(self) -> int:
        '''e.g. 3²×11¹ -> 3*2=6'''
        return prod(q+1 for _, q in self._factors[:self.factors_count])

    def sum_of_factors(self) -> int:
        '''return the sum of all factors. e.g. 6 -> 1+2+3+6=12'''
        return prod(
            (pow(factor, exp+1)-1)//(factor-1) for factor, exp in self._factors[:self.factors_count]
        )

    def is_prime(self) -> bool:
        '''return whether this is a prime number'''
        if self.i<2:
            return False
        return self.factors_count == 1 and self._factors[0].exp == 1

_decompose = clib.decompose
_decompose.argtypes = [c_uint32]
_decompose.restype = Factorized

__all__ = [
    'Pow', 'Factorized'
]

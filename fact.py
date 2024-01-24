'''This module allows you to prime factorize a number.'''

from ctypes import CDLL, c_uint32, Structure, c_uint64, c_int16, POINTER
from typing import Sequence, Self, Iterator, SupportsInt
from itertools import product
from math import prod

PERFECT_NUMBERS = {6, 28, 496, 8128, 33550336, 8589869056, 0x1ffffc0000, 0x1fffffffc0000000}
UPPER = ('⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹')
UPPER_SKIP1 = ('⁰','','²','³','⁴','⁵','⁶','⁷','⁸','⁹')

pi = '×'.join
connect = ''.join
bits = int.bit_length


def _n0_s1_upper(_i: int, /) -> str:
    '''return upper form of input number (>=0)'''
    if _i < 10 :
        return UPPER_SKIP1[_i]
    return connect(UPPER[(ord(o)-48)%10] for o in str(_i))

def upper(_i: int, /) -> str:
    '''return upper form of input number'''
    if _i<0:
        return '⁻'+connect(UPPER[(ord(o)-48)%10] for o in str(-_i))
    return connect(UPPER[(ord(o)-48)%10] for o in str(_i))

clib = CDLL('./fact.so')
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

    def __init__(self, base: int, exp: int) -> None:
        super().__init__(base, exp)

    def __iter__(self):
        yield self.base
        yield self.exp

    def __index__(self) -> int:
        return pow(self.base, self.exp)

    def __getitem__(self, _x: int) -> int:
        return (self.base, self.exp)[_x]

    def __repr__(self) -> str:
        return f'{self.base}{upper(self.exp)*(self.exp!=1)}'

def _factors_of_prime_pow(pp: Pow) -> list[int]:
    base, exp = pp
    return [pow(base, exp_) for exp_ in range(exp+1)]


class Factorized(Structure):
    '''Store prime factors of i, support [0, 2^50)'''
    __slots__ = ('i', 'prime_factors_count', '__factors')

    i: int
    prime_factors_count: int
    __factors: Sequence[Pow]
    _fields_ =[
        ('i', c_uint64),
        ('prime_factors_count', c_uint32),
        ('_Factorized__factors', POINTER(Pow))
    ]

    def __new__(cls, _i: int | Self, /) -> Self:
        if isinstance(_i, Factorized):
            return _i
        if bits(_i) > 50: # assert _i<2^50
            raise ValueError('Too large to factorize.')
        if _i<0:
            raise ValueError('Integer should be greater than 0.')
        return _decompose(_i)

    def __str__(self) -> str:
        return f'{self.i}: {pi(f'{f.base}{_n0_s1_upper(f.exp)}'
                            for f in self.__factors[:self.prime_factors_count])}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.i})'

    def __del__(self) -> None:
        free_ptr(self.__factors)

    def __iter__(self) -> Iterator[Pow]:
        return iter(self.__factors[:self.prime_factors_count])

    def __getitem__(self, _i, /) -> Pow:
        if _i >= self.prime_factors_count:
            raise IndexError('Index out of range.')
        return self.__factors[_i]

    def __index__(self) -> int:
        return self.i

    def __mul__(self, _r: Self | SupportsInt) -> Self:
        r = Factorized(int(_r))
        new_i = self.i*r.i
        if bits(new_i)>64:
            raise ValueError('Too large to multiply.')
        return _mul(self, r)

    def prime_factors(self) -> list[int]:
        '''return all the prime factors of the number'''
        return [base for base, _ in self.__factors[:self.prime_factors_count]]

    def factors(self) -> set[int]:
        '''get all the factors of the number'''
        return {
            prod(factor) for factor in
            product(*map(_factors_of_prime_pow, self.__factors[:self.prime_factors_count]))
        }

    def factors_count(self) -> int:
        '''e.g. 3²×11¹ -> 3*2=6'''
        return prod(q+1 for _, q in self.__factors[:self.prime_factors_count])

    def factors_sum(self) -> int:
        '''return the sum of all factors. e.g. 6 -> 1+2+3+6=12'''
        return prod(
            (pow(prime, exp+1)-1)//(prime-1) for
            prime, exp in self.__factors[:self.prime_factors_count]
        )

    def is_prime(self) -> bool:
        '''return whether this is a prime number'''
        return self.i > 1 and self.prime_factors_count == 1 and self.__factors[0].exp == 1

    def is_square(self) -> bool:
        '''return whether this is a perfect square number'''
        return self.i < 2 or not \
               any(exp & 1 for exp, _ in self.__factors[:self.prime_factors_count])

    def is_perfect_number(self) -> bool:
        '''return whether this is a perfect number'''
        return self.i in PERFECT_NUMBERS

_decompose = clib.decompose
_decompose.argtypes = [c_uint64]
_decompose.restype = Factorized
_mul = clib.mul
_mul.argtypes = [Factorized, Factorized]
_mul.restype = Factorized

__all__ = [
    'Pow', 'Factorized'
]

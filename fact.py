'''This module allows you to prime factorize a number.'''

from ctypes import CDLL, c_uint32, Structure, c_uint64, c_int16, c_uint16, POINTER, byref
from typing import Sequence, Self, Iterator, SupportsIndex
from itertools import product
from math import prod, gcd

PERFECT_NUMBERS = {6, 28, 496, 8128, 33550336, 8589869056, 0x1ffffc0000, 0x1fffffffc0000000}
UPPER = ('⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹')
UPPER_SKIP1 = ('⁰','','²','³','⁴','⁵','⁶','⁷','⁸','⁹')

pi = '×'.join
connect = ''.join
bits = int.bit_length


def _n0_upper(_i: int, /) -> str:
    '''return upper form of input number (>=0)'''
    if _i < 10 :
        return UPPER[_i]
    return connect(UPPER[(ord(o)-48)%10] for o in str(_i))

def _n0_s1_upper(_i: int, /) -> str:
    '''return upper form of input number (>=0), skip 1'''
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

    i: int
    prime_factors_count: int
    __factors: Sequence[Pow]
    _fields_ =[
        ('i', c_uint64),
        ('prime_factors_count', c_uint32),
        ('_Factorized__factors', POINTER(Pow))
    ]

    def __new__(cls, _i: int | Self, /):
        if isinstance(_i, Factorized):
            return _copy(_i)
        if bits(_i) > 50: # assert _i<2^50
            raise ValueError('Too large to factorize.')
        if _i<0:
            raise ValueError('Integer should be greater than 0.')
        return _decompose(_i)

    def __init__(self, _i: int | Self, /) -> None:
        pass

    def __str__(self) -> str:
        return f'{self.i}: {pi(f'{base}{_n0_s1_upper(exp)}'
                            for base, exp in self.__factors[:self.prime_factors_count])}'

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

    def __mul__(self, _r: 'Factorized | int') -> 'Factorized':
        r = _r if isinstance(_r, Factorized) else Factorized(_r)
        if bits(self.i)+bits(r.i)>64:
            raise ValueError('Too large to multiply.')
        return _mul(self, r)

    def __pow__(self, exp: int, mod: None | int=None) -> 'Factorized':
        assert exp >=0, 'not support nagative power'
        if mod:
            return Factorized(pow(self.i, exp, mod))
        return _pow(self, exp)

    def __ipow__(self, exp: int) -> 'Factorized':
        assert exp >=0, 'not support nagative power'
        _ipow(byref(self), exp)
        return self

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

    def is_coprime_with(self, _r: SupportsIndex, /) -> bool:
        '''return whether this is coprime with given number'''
        return gcd(self, _r) == 1

    def gcd_with(self, _r: 'Factorized | int', /) -> 'Factorized':
        '''return the greatest common divisor of self and the other'''
        r = _r if isinstance(_r, Factorized) else Factorized(_r)
        if self.i and r.i:
            return _gcd(self, r)
        if self.i:
            return _copy(self)
        if r.i:
            return _copy(r)
        raise ValueError('gcd(0, 0) = inf.')

    def expanded_str(self, skip1: bool = True) -> str:
        '''e.g. 50 -> 2×5² if skip1 else 2¹×5²'''
        up_func = _n0_s1_upper if skip1 else _n0_upper
        return pi(
            f'{base}{up_func(exp)}' for base, exp in self.__factors[:self.prime_factors_count]
        )


_decompose = clib.decompose
_decompose.argtypes = [c_uint64]
_decompose.restype = Factorized
_copy = clib.copy
_copy.argtypes = [Factorized]
_copy.restype = Factorized
_mul = clib.mul
_mul.argtypes = [Factorized, Factorized]
_mul.restype = Factorized
_gcd = clib.gcd
_gcd.argtypes = [Factorized, Factorized]
_gcd.restype = Factorized
_pow = clib._pow   # pylint: disable = protected-access
_pow.argtypes = [Factorized, c_uint32]
_pow.restype = Factorized
_ipow = clib._ipow # pylint: disable = protected-access
_ipow.argtypes = [POINTER(Factorized), c_uint32]
_ipow.restype = None

__p16_p = clib.get_prime16_p
__p16_p.argtypes = []
__p16_p.restype = POINTER(c_uint16)

PRIME16: c_int16*6542 = __p16_p()[:6542]

__all__ = [
    'Pow', 'Factorized', 'PRIME16'
]

'''Shared tools and base classes between the module'''


from itertools import product
from math import gcd, prod
from typing import Iterator, Self, Sequence, SupportsIndex

from kind_of_int import have_int, to_int


class PowBase(to_int(lambda self: pow(*self))):
    '''Base of pow-like class'''

    base: int
    exp: int

    def __iter__(self) -> Iterator[int]:
        yield self.base
        yield self.exp

    def __getitem__(self, _i: SupportsIndex) -> int:
        return (self.base, self.exp)[_i]

    def __eq__(self, __r: Self) -> bool:
        return self.base == __r.base and self.exp == __r.exp



POW_2_50 = 1125899906842624
POW_2_32 = 4294967296
PERFECT_NUMBERS = {6, 28, 496, 8128, 33550336, 8589869056, 0x1ffffc0000, 0x1fffffffc0000000}
UPPER = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')
UPPER_SKIP1 = ('⁰', '', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')

pi = '×'.join
connect = ''.join
bits = int.bit_length


def _n0_upper(_i: int, /) -> str:
    '''return upper form of input number (>=0)'''
    if _i < 10:
        return UPPER[_i]
    return connect(UPPER[(ord(o) - 48) % 10] for o in str(_i))


def _n0_s1_upper(_i: int, /) -> str:
    '''return upper form of input number (>=0), skip 1'''
    if _i < 10:
        return UPPER_SKIP1[_i]
    return connect(UPPER[(ord(o) - 48) % 10] for o in str(_i))


def upper(_i: int, /) -> str:
    '''return upper form of input number'''
    if _i < 0:
        return '⁻' + connect(UPPER[(ord(o) - 48) % 10] for o in str(-_i))
    return connect(UPPER[(ord(o) - 48) % 10] for o in str(_i))


def _factors_of_prime_pow(pp: PowBase) -> list[int]:
    base, exp = pp
    return [pow(base, exp_) for exp_ in range(exp + 1)]


class FactedBase[P: PowBase](have_int('i')):
    '''Having essentialmathod and attributes of a factorized number'''
    i: int
    prime_factors_count: int
    prime_factors_pows: Sequence[P]


    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.i})'

    def __iter__(self) -> Iterator[P]:
        return iter(self.prime_factors_pows)

    def __getitem__(self, __index: SupportsIndex) -> P:
        return self.prime_factors_pows[__index]

    def prime_factors(self) -> list[int]:
        '''return all the prime factors of the number'''
        return [base for base, _ in self.prime_factors_pows]

    def factors(self) -> set[int]:
        '''get all the factors of the number'''
        return {
            prod(factor) for factor in
            product(*map(_factors_of_prime_pow, self.prime_factors_pows))
        }

    def factors_count(self) -> int:
        '''e.g. 3²×11¹ -> 3*2=6'''
        return prod(q + 1 for _, q in self.prime_factors_pows)

    def factors_sum(self) -> int:
        '''return the sum of all factors. e.g. 6 -> 1+2+3+6=12'''
        return prod(
            (pow(prime, exp + 1) - 1) // (prime - 1) for
            prime, exp in self.prime_factors_pows
        )

    def is_prime(self) -> bool:
        '''return whether this is a prime number'''
        return self.i > 1 and self.prime_factors_count == 1 and self.prime_factors_pows[0].exp == 1

    def is_square(self) -> bool:
        '''return whether this is a perfect square number'''
        return self.i < 2 or not \
               any(exp & 1 for exp, _ in self.prime_factors_pows)

    def is_perfect_number(self) -> bool:
        '''return whether this is a perfect number'''
        return self.i in PERFECT_NUMBERS

    def is_coprime_with(self, _r: SupportsIndex, /) -> bool:
        '''return whether this is coprime with given number'''
        return gcd(self, _r) == 1

    def expression(self, skip1: bool = True) -> str:
        '''e.g. 50 -> 2×5² if skip1 else 2¹×5²'''
        up_func = _n0_s1_upper if skip1 else _n0_upper
        return pi(
            f'{base}{up_func(exp)}' for base, exp in self.prime_factors_pows
        )

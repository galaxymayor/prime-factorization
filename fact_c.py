'''This module allows you to prime factorize a number using c shared library.'''


from ctypes import c_uint32, Structure, c_uint64, c_int16, POINTER
from typing import Callable, Self, Iterator, final

try:
    from .base_tool import PowBase, FactedBase, _n0_s1_upper, pi, bits
    from .new_fact import \
        decompose as dcp, free_facted, \
            copy as __copy, mul as __mul, gcd as __gcd, _pow as __pow, _ipow, \
                PRIME16, SQ_PRIME16
except ImportError:
    from base_tool import PowBase, FactedBase, _n0_s1_upper, pi, bits
    from new_fact import \
        decompose as dcp, free_facted, \
            copy as __copy, mul as __mul, gcd as __gcd, _pow as __pow, _ipow, \
                PRIME16, SQ_PRIME16


@final
class N0PowC(Structure, PowBase):
    '''Represent base^exp where base, exp isinstanceof N0'''

    base: int
    exp: int

    _fields_ = [
        ('base', c_uint64),
        ('exp', c_int16),
    ]


    __init__: Callable[[int, int], None]

    def __iter__(self):
        yield self.base
        yield self.exp

    def __index__(self) -> int:
        return pow(self.base, self.exp)

    def __int__(self) -> int:
        return pow(self.base, self.exp)

    def __getitem__(self, _x: int) -> int:
        return (self.base, self.exp)[_x]

    def __str__(self) -> str:
        return f'{self.base}{_n0_s1_upper(self.exp)}'

    def __format__(self, __format_spec: str) -> str:
        if __format_spec in {'', 's'}:
            return str(self)
        if __format_spec == 'py':
            return f'{self.base}**{self.exp}'
        if __format_spec == 'm':
            return f'{self.base}^{self.exp}'
        if __format_spec == 'f':
            return f'{self.base}{_n0_s1_upper(self.exp)}'
        if __format_spec.startswith('str-'):
            self_f, str_f = __format_spec.split('-', 2)[1:]
            return format(f'{self:{self_f}}', str_f)
        raise ValueError(f'Unknown format specifier {__format_spec!r}')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.base}, {self.exp})'

    def __eq__(self, __r: Self) -> bool:
        return self.base == __r.base and self.exp == __r.exp


@final
class FactorizedC(Structure, FactedBase):
    '''Store prime factors of i, support [0, 2^50)'''

    __slots__ = ('prime_factors_pows', 'address')

    i: int
    prime_factors_count: int
    prime_factors_pows: list[N0PowC]
    address: int
    _fields_ = [
        ('i', c_uint64),
        ('prime_factors_count', c_uint32),
        ('_FactorizedC__factors', POINTER(N0PowC))
    ]

    def __new__(cls, _i: int, /):
        return decompose(_i)

    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def __str__(self) -> str:
        return f'{self.i}: {pi(f'{base}{_n0_s1_upper(exp)}'
                            for base, exp in self.prime_factors_pows)}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.i})'

    def __del__(self) -> None:
        free_facted(self.address)

    def __iter__(self) -> Iterator[N0PowC]:
        return iter(self.prime_factors_pows)

    def __getitem__(self, _i, /) -> N0PowC:
        return self.prime_factors_pows[_i]

    def __index__(self) -> int:
        return self.i

    def __mul__(self, _r: 'FactorizedC | int') -> 'FactorizedC':
        r = _r if isinstance(_r, FactorizedC) else decompose(_r)
        if bits(self.i) + bits(r.i) > 64:
            raise OverflowError('Too large to multiply.')
        return _mul(self, r)

    def __pow__(self, exp: int, mod: None | int = None) -> 'FactorizedC':
        if mod:
            return decompose(pow(self.i, exp, mod))

        if (bits(self.i) + 1) * exp > 64:
            raise OverflowError('Too large to power.')
        return _pow(self, exp)

    def __ipow__(self, exp: int) -> Self:
        if (bits(self.i) + 1) * exp > 64:
            raise OverflowError('Too large to power.')
        _ipow(self.address, exp)
        return self

    def gcd_with(self, _r: 'FactorizedC | int', /) -> 'FactorizedC':
        '''return the greatest common divisor of self and the other'''
        r = _r if isinstance(_r, FactorizedC) else decompose(_r)
        if self.i and r.i:
            return _gcd(self, r)
        if self.i:
            return _copy(self)
        if r.i:
            return _copy(self)
        raise ValueError('gcd(0, 0) = inf.')

    @staticmethod
    def copy(f: 'FactorizedC') -> 'FactorizedC':
        '''return a copy of FactorizedC instance'''
        # pylint: disable = protected-access
        new = get_facted(address := __copy(f.address))
        new.address = address
        new.prime_factors_pows = new._FactorizedC__factors[:new.prime_factors_count]
        return new


type FactedFunc[**P] = Callable[P, FactorizedC]


def _cfunc_facted_initfy[**PS](func: FactedFunc[PS]) -> FactedFunc[PS]:
    # pylint: disable = protected-access
    def __f(*args) -> FactorizedC:
        facted: FactorizedC = func(*args)  #type: ignore
        facted.prime_factors_pows = facted._FactorizedC__factors[:facted.prime_factors_count]
        return facted
    return __f  #type: ignore


def _1arg_facted_initfy[T](func: FactedFunc[T]) -> FactedFunc[T]:
    # pylint: disable = protected-access
    def __f(arg) -> FactorizedC:
        facted: FactorizedC = func(arg)  #type: ignore
        facted.prime_factors_pows = facted._FactorizedC__factors[:facted.prime_factors_count]
        return facted
    return __f  #type: ignore


get_facted = FactorizedC.from_address


def _decompose(i: int, /) -> FactorizedC:
    '''No cache. Input a number prime factorizes it, support range [0, 2^64)'''
    # pylint: disable = protected-access
    facted = get_facted(address := dcp(i))
    facted.prime_factors_pows = facted._FactorizedC__factors[:facted.prime_factors_count]
    facted.address = address
    return facted


_fact_cache = [_decompose(i) for i in range(512)]


class TLEWarning(UserWarning):
    '''To warn it might consume too much time'''


def decompose(i: int, /) -> FactorizedC:
    '''\
        Cached 0-511.
        Input a number prime factorizes it.
        time safe range [0, 2^52] (won\'t check).'''
    # pylint: disable = protected-access
    if 0 <= i < 512:
        return _fact_cache[i]
    facted = get_facted(address := dcp(i))
    facted.prime_factors_pows = facted._FactorizedC__factors[:facted.prime_factors_count]
    facted.address = address
    return facted


def _copy(f: FactorizedC) -> FactorizedC:
    # pylint: disable = protected-access
    new = get_facted(address := __copy(f.address))
    new.address = address
    new.prime_factors_pows = new._FactorizedC__factors[:new.prime_factors_count]
    return new


def _mul(a: FactorizedC, b: FactorizedC) -> FactorizedC:
    # pylint: disable = protected-access
    f = get_facted(address := __mul(a.address, b.address))
    f.address = address
    f.prime_factors_pows = f._FactorizedC__factors[:f.prime_factors_count]
    return f


def _gcd(a: FactorizedC, b: FactorizedC) -> FactorizedC:
    # pylint: disable = protected-access
    f = get_facted(address := __gcd(a.address, b.address))
    f.address = address
    f.prime_factors_pows = f._FactorizedC__factors[:f.prime_factors_count]
    return f

def _pow(base: FactorizedC, exp: int) -> FactorizedC:
    # pylint: disable = protected-access
    f = get_facted(address := __pow(base.address, exp))
    f.address = address
    f.prime_factors_pows = f._FactorizedC__factors[:f.prime_factors_count]
    return f


__all__ = [
    'N0PowC', 'FactorizedC', 'PRIME16', 'SQ_PRIME16', 'decompose'
]

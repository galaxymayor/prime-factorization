'''Factrorizing a number using python code.'''
from typing import Self, overload
try:
    from .base_tool import upper, _n0_s1_upper, pi, PowBase, FactedBase
    from .fact_c import PRIME16, SQ_PRIME16, FactorizedC, decompose
except ImportError:
    from base_tool import upper, _n0_s1_upper, pi, PowBase, FactedBase
    from fact_c import PRIME16, SQ_PRIME16, FactorizedC, decompose


_new_tuple = tuple.__new__


class IPow(tuple[int, int], PowBase):
    '''IPow(base, exp) means base**exp, where base, exp ∈ Z'''
    base: int
    exp: int

    def __new__(cls, base: int, exp: int):
        # assert isinstance(base, int) and isinstance(exp, int)
        return _new_tuple(cls, (base, exp))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{super().__repr__()}'

    def __str__(self) -> str:
        return f'{self[0]}{upper(self[1]) if self[1] !=1 else ''}'

    def __getattr__(self, attr: str):
        if attr == 'base':
            return self[0]
        if attr == 'exp':
            return self[1]
        raise AttributeError(
            f'class \'{self.__class__.__name__}\' does not have attribute \'{attr}\'')

    def __int__(self) -> int:
        return pow(*self)

    def __index__(self) -> int:
        return pow(*self)


class N0Pow(IPow):
    '''IPow(base, exp), where base, exp ≥ 0'''

    def __new__(cls, base: int, exp: int):
        assert isinstance(base, int) and isinstance(exp, int)
        assert base >= 0 and exp >= 0
        return _new_tuple(cls, (base, exp))

    def __str__(self) -> str:
        return f'{self[0]}{_n0_s1_upper(self[1])}'


def _factors_of_prime_pow(pp: N0Pow) -> list[int]:
    base, exp = pp
    return [pow(base, exp_) for exp_ in range(exp + 1)]


class FactorizedPy(FactedBase):
    '''prime factorizes i, support [0, 2^50)'''

    __slots__ = ('i', 'prime_factors_count', 'prime_factors_pows')
    i: int
    prime_factors_count: int
    prime_factors_pows: tuple[N0Pow, ...]

    @overload
    def __init__(self, i: int, /) -> None: ...

    @overload
    def __init__(self, i: Self | FactorizedC, /) -> None: ...

    @overload
    def __init__(self, i: int, pfc: int, pfs: tuple[N0Pow, ...]) -> None: ...

    def __init__(self, i: int | Self | FactorizedC,
                 pfc: int | None = None, pfs: tuple[N0Pow, ...] | None = None) -> None:
        if isinstance(i, self.__class__):
            self.i = i.i
            self.prime_factors_count = i.prime_factors_count
            self.prime_factors_pows = i.prime_factors_pows
            return

        if isinstance(i, FactorizedC):
            self.i = i.i
            self.prime_factors_count = i.prime_factors_count
            self.prime_factors_pows = tuple(N0Pow(base, exp) for base, exp in i)
            return

        if i < 0:
            raise OverflowError(f'{i} is out of domain.')

        self.i = i
        if pfc:
            assert isinstance(pfc, int)
            assert isinstance(pfs, tuple)
            self.prime_factors_count = pfc
            self.prime_factors_pows = pfs
            return

        if i < 512:
            self.prime_factors_count = _fact_cache[i].prime_factors_count
            self.prime_factors_pows = _fact_cache[i].prime_factors_pows
        elif i < 524288:
            self.prime_factors_pows = fs = _factorize_u32(i)
            self.prime_factors_count = len(fs)
        else:
            fs = decompose(i)
            self.prime_factors_count = fs.prime_factors_count
            self.prime_factors_pows = tuple(N0Pow(base, exp) for base, exp in fs)

    def __str__(self) -> str:
        return f'{self.i}: {pi(f'{base}{_n0_s1_upper(exp)}'
                            for base, exp in self.prime_factors_pows)}'


    # def __mul__(self, _r: Sequence[N0Pow | PowC]) -> Self:


_fact_cache = [FactorizedPy(decompose(i)) for i in range(512)]


def _factorize_u32(i: int) -> tuple[N0Pow, ...]:
    ans: list[N0Pow] = []
    add = ans.append
    exp: int
    for p, sqp in zip(PRIME16, SQ_PRIME16):
        if sqp>i:
            break
        exp = 0
        while not i % p:
            i //= p
            exp += 1
        if exp:
            add(_new_tuple(N0Pow, (p, exp)))
    if i != 1:
        add(_new_tuple(N0Pow, (i, 1)))
    return tuple(ans)

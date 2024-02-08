'''test if it works'''
from math import prod
from itertools import chain
from unittest import main, TestCase
from fact_c import FactorizedC, N0PowC, decompose

_HIGH_START = 0x00_0f_ff_ff_ff_ff_ff_80
_HIGH_END   = 0x00_10_00_00_00_00_00_00
_HIGH_RANGE = range(_HIGH_START, _HIGH_END)
_MID_RANGE = range((1<<32)-128, 1<<32)
_LOW_RANGE = range(128)


class TestFuncDecompose(TestCase):
    '''Test decompose'''

    def test_class(self):
        '''test the output class matches type hints'''
        self.assertEqual(decompose(10).__class__, FactorizedC)

    def test_domain(self):
        with self.subTest(cat='out of domain'):
            self.assertRaises(OverflowError, decompose, 1<<64)
            self.assertRaises(OverflowError, decompose, -1)
        i = 2**63
        while i:
            with self.subTest(cat='in domain', i=bin(i)):
                self.assertEqual(decompose(i), i)
            i>>=1


class TestN0PowC(TestCase):
    '''Test class N0PowC'''
    def test_pow_repr(self):
        '''test if it represents correctly'''
        sub = self.subTest
        as_eq = self.assertEqual
        for i in range(5):
            for j in range(5):
                with sub(base=i, exp=j):
                    as_eq(eval(repr(N0PowC(i, j))), N0PowC(i, j))

    def test_pow_int(self):
        '''test if Pow -> int no problem'''
        sub = self. subTest
        as_eq = self.assertEqual
        for i in range(11):
            for j in range(11):
                with sub(base=i, exp=j):
                    as_eq(pow(i, j), int(N0PowC(i, j)))


class TestFactorizedC(TestCase):
    '''Test class FactorizedC'''


    def test_repr(self):
        sub = self.subTest
        as_eq = self.assertEqual
        for i in chain(_LOW_RANGE, _HIGH_RANGE):
            with sub(i=i):
                as_eq(eval(repr(FactorizedC(i))), FactorizedC(i))

    def test_mul(self):
        '''test if it multipies correctly'''
        sub = self.subTest
        as_eq = self.assertEqual
        for i in range(1, 17):
            for j in range(2, 17):
                facted0 = FactorizedC(i) * j
                facted1 = FactorizedC(i*j)
                with sub(i=i, j=j):
                    as_eq(facted0, i*j)
                    as_eq(facted0.prime_factors_count, facted1.prime_factors_count)
                    for p0, p1 in zip(facted0, facted1):
                        as_eq(p0, p1)

    def test_pow(self):
        '''test if it powers correctly'''
        sub = self.subTest
        as_eq = self.assertEqual
        for base in range(10):
            f = FactorizedC(base)
            as_eq(f**0, 1)
            for exp in range(1, 5):
                fp = f**exp
                with sub(base=base, exp=exp):
                    as_eq(f.prime_factors_count, fp.prime_factors_count)
                    for i, j in zip(f, fp):
                        as_eq(i.base, j.base)
                        as_eq(i.exp * exp, j.exp)

    def test_int_correct(self):
        '''test if it represents int correctly'''
        sub = self.subTest
        as_eq = self.assertEqual
        as_gt = self.assertGreater
        as_lt = self.assertLess
        for i in range(128):
            facted = FactorizedC(i)
            with sub(i=i):
                as_eq(facted, i)
                as_gt(facted, i-1)
                as_lt(facted, i+1)
                as_eq(facted, int(facted))

    def test_domain(self):
        '''test if it raises error when out of domain'''
        sub = self.subTest
        with sub(i=-1):
            self.assertRaises(OverflowError, FactorizedC, -1)
        with sub(i=2**64):
            self.assertRaises(OverflowError, FactorizedC, 2**64)

    def test_factorizes_correct(self):
        '''test if it factorizes correctly'''
        sub = self.subTest
        as_eq = self.assertEqual
        for i in chain(_LOW_RANGE, _HIGH_RANGE):
            facted = FactorizedC(i)
            with sub(i=i):
                as_eq(
                    prod(map(int, facted)),
                    i
                )

    def test_factors_correct(self):
        '''test if all factors match'''
        sub = self.subTest
        as_eq = self.assertEqual
        f_count = FactorizedC.factors_count
        facts = FactorizedC.factors
        for i in chain(_LOW_RANGE, _HIGH_RANGE):
            facted = FactorizedC(i)
            with sub(i=i):
                as_eq(
                    f_count(facted),
                    len(fs := facts(facted))
                )
                for f in fs:
                    as_eq(f and (i % f), 0)

    def test_some_primes(self):
        '''enumerate some primes and test if it can identify them'''
        sub = self.subTest
        as_t = self.assertTrue

        for i in (2, 7, 13, 31, 1125899906842589, 1125899906842597, 18446744073709551557):
            with sub(i=i):
                as_t(FactorizedC(i).is_prime())

    def test_some_composites(self):
        '''enum some composite numbers and test if it factorizes correctly'''
        sub = self.subTest
        as_eq = self.assertEqual

        enums: list[tuple[int, tuple[tuple[int, int], ...]]] = [
            (9, ((3, 2), )),
            (51, ((3, 1), (17, 1))),
            (100, ((2, 2), (5, 2))),
            (1125899906842623, ((3, 1), (11, 1), (31, 1), (251, 1), (601, 1), (1801, 1), (4051, 1)))
        ]

        for i, ans in enums:
            with sub(i=i):
                facted = FactorizedC(i)
                as_eq(facted.prime_factors_count, len(ans))
                for (fb, fe), (ab, ae) in zip(facted, ans):
                    as_eq(fb, ab)
                    as_eq(fe, ae)

if __name__ == '__main__':
    main()

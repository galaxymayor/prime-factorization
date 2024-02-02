'''test if it works'''
from math import prod
from itertools import chain
from unittest import main, TestCase
from fact import Factorized

_HIGH_START = 0x00_03_ff_ff_ff_ff_fe_00
_HIGH_END   = 0x00_04_00_00_00_00_00_00

class TestFactorized(TestCase):
    '''Test class Factorized'''
    def test_fact_correct(self):
        '''test if it factorizes correctly'''
        sub = self. subTest
        for i in chain(range(512), range(_HIGH_START, _HIGH_END)):
            facted = Factorized(i)
            with sub(i=i):
                self.assertEqual(
                    prod(map(int, facted)),
                    i
                )

    def test_factors_correct(self):
        '''test if all factors match'''
        sub = self. subTest
        for i in chain(range(512), range(_HIGH_START, _HIGH_END)):
            facted = Factorized(i)
            with sub(i=i):
                self.assertEqual(
                    facted.factors_count(),
                    len(fs := facted.factors())
                )
                for f in fs:
                    self.assertEqual(f and (i % f), 0)

if __name__ == '__main__':
    main()

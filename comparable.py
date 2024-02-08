'''int-like base class'''

from typing import Any, Callable, SupportsIndex

get_attr = object.__getattribute__


def have_int(int_name: str):
    '''while input the inside int name,\
       return a class implements comparative operators for you to inherit from'''
    class HaveInt:
        '''implement comparative operators form inside int'''
        __slots__ = ()
        def __int__(self) -> int:
            return get_attr(self, int_name)
        def __index__(self) -> int:
            return get_attr(self, int_name)
        def __gt__(self, __r: SupportsIndex) -> bool:
            return get_attr(self, int_name) > int(__r)
        def __lt__(self, __r: SupportsIndex) -> bool:
            return get_attr(self, int_name) < int(__r)
        def __ge__(self, __r: SupportsIndex) -> bool:
            return get_attr(self, int_name) >= int(__r)
        def __le__(self, __r: SupportsIndex) -> bool:
            return get_attr(self, int_name) <= int(__r)
    return HaveInt


def to_int(func: Callable[[Any], int]):
    '''while input the get int func,\
       return a class implements comparative operators for you to inherit from'''
    class ToInt:
        '''implement comparative operators form given func'''
        __slots__ = ()
        __int__ = func
        __index__ = func
        def __gt__(self, __r: SupportsIndex) -> bool:
            return func(self) > int(__r)
        def __lt__(self, __r: SupportsIndex) -> bool:
            return func(self) < int(__r)
        def __ge__(self, __r: SupportsIndex) -> bool:
            return func(self) >= int(__r)
        def __le__(self, __r: SupportsIndex) -> bool:
            return func(self) <= int(__r)
    return ToInt

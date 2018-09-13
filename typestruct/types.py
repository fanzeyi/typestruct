# -*- coding: utf-8 -*-

from typing import NewType, List

Bool = NewType('bool', bool)

int8 = NewType('int8', int)
int16 = NewType('int16', int)
int32 = NewType('int32', int)
int64 = NewType('int64', int)

uint8 = NewType('uint8', int)
uint16 = NewType('uint16', int)
uint32 = NewType('uint32', int)
uint64 = NewType('uint64', int)


def Slice(length):
    return NewType('[{}]'.format(length), List[int])


def Varlength(func):
    ttype = NewType('{}', List[int])
    ttype.__dyn__ = func
    return ttype


__all__ = ["Bool", "int8", "int16", "int32", "int64", "uint8", "uint16",
           "uint32", "uint64", "Slice", "Varlength"]

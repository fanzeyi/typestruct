# -*- coding: utf-8 -*-

import typing
import struct
from enum import Enum

from typestruct.types import Bool, int8, int16, int32, int64, uint8, uint16, \
    uint32, uint64


class Endian(Enum):
    NATIVE = '@'
    LITTLE_ENDIAN = '<'
    BIG_ENDIAN = '>'


def get_struct_type(obj, ttype):
    if ttype == Bool:
        return "?"
    elif ttype == int8:
        return "b"
    elif ttype == int16:
        return "h"
    elif ttype == int32:
        return "i"
    elif ttype == int64:
        return "q"
    elif ttype == uint8:
        return "B"
    elif ttype == uint16:
        return "H"
    elif ttype == uint32:
        return "I"
    elif ttype == uint64:
        return "Q"
    else:
        name = ttype.__name__

        if not name:
            raise Exception()

        if name == "{}":
            length = ttype.__dyn__(obj)
            return "{}s".format(length)
        elif name[0] == "[" and name[-1] == "]":
            length = int(name[1:-1])
            return "{}s".format(length)
    raise Exception()


class Packet:
    def serialize(self, endian=Endian.NATIVE):
        hints = typing.get_type_hints(self)
        struct_format = self._struct_format(hints, endian)
        values = [getattr(self, key) for key in hints.keys()]

        return struct.pack(struct_format, *values)

    @classmethod
    def deserialize(cls, buf, endian=Endian.NATIVE):
        hints = typing.get_type_hints(cls)
        obj = cls.__new__(cls)

        for key, ttype in hints.items():
            format_string = get_struct_type(obj, ttype)
            size = struct.calcsize(format_string)
            value = struct.unpack(endian.value + format_string, buf[:size])[0]
            buf = buf[size:]
            setattr(obj, key, value)

        return obj

    def _struct_format(self, hints, endian) -> str:
        result = [endian.value]

        for ttype in hints.values():
            result.append(get_struct_type(self, ttype))

        return "".join(result)

# -*- coding: utf-8 -*-

import unittest
from typestruct import Packet, types, Endian
from dataclasses import dataclass


@dataclass
class ExamplePacket(Packet):
    bool: types.Bool
    int8: types.int8
    int16: types.int16
    int32: types.int32
    int64: types.int64
    bool2: types.Bool
    uint8: types.uint8
    uint16: types.uint16
    uint32: types.uint32
    uint64: types.uint64
    array: types.Slice(2)
    vararray: types.Varlength(lambda s: s.int8)


@dataclass
class Int64Packet(Packet):
    value: types.int64


@dataclass
class VarlengthPacket(Packet):
    length: types.int8
    value: types.Varlength(lambda x: x.length)


class TestSerialization(unittest.TestCase):
    def test_serialization(self):
        packet = ExamplePacket(True,
                               0x01, 0x0102, 0x01020304, 0x0102030405060708,
                               False,
                               0x01, 0x0102, 0x01020304, 0x0102030405060708,
                               b"\xde\xad", b"\x01")

        self.assertEqual(packet.serialize(), b'\x01\x01\x02\x01\x04\x03\x02'
                         b'\x01\x08\x07\x06\x05\x04\x03\x02\x01\x00\x01\x02'
                         b'\x01\x04\x03\x02\x01\x08\x07\x06\x05\x04\x03\x02'
                         b'\x01\xde\xad\x01')

    def test_big_endian(self):
        packet = Int64Packet(0x0102030405060708)
        self.assertEqual(packet.serialize(endian=Endian.BIG_ENDIAN),
                         b'\x01\x02\x03\x04\x05\x06\x07\x08')

    def test_little_endian(self):
        packet = Int64Packet(0x0102030405060708)
        self.assertEqual(packet.serialize(endian=Endian.LITTLE_ENDIAN),
                         b'\x08\x07\x06\x05\x04\x03\x02\x01')

    def test_varlength(self):
        packet = VarlengthPacket(2, b"\xde\xad")
        self.assertEqual(packet.serialize(endian=Endian.BIG_ENDIAN),
                         b"\x02\xde\xad")
        packet = VarlengthPacket(4, b"\xde\xad\xbe\xef")
        self.assertEqual(packet.serialize(endian=Endian.BIG_ENDIAN),
                         b"\x04\xde\xad\xbe\xef")


class TestDeserialization(unittest.TestCase):
    def test_deserialization(self):
        packet = ExamplePacket.deserialize(b'\x01\x01\x02\x01\x04\x03\x02\x01'
                                           b'\x08\x07\x06\x05\x04\x03\x02\x01'
                                           b'\x00\x01\x02\x01\x04\x03\x02\x01'
                                           b'\x08\x07\x06\x05\x04\x03\x02\x01'
                                           b'\xde\xad\x01')
        target = ExamplePacket(True,
                               0x01, 0x0102, 0x01020304, 0x0102030405060708,
                               False,
                               0x01, 0x0102, 0x01020304, 0x0102030405060708,
                               b"\xde\xad", b"\x01")
        self.assertEqual(packet, target)

    def test_big_endian(self):
        packet = Int64Packet.deserialize(b'\x01\x02\x03\x04\x05\x06\x07\x08',
                                         endian=Endian.BIG_ENDIAN)
        self.assertEqual(packet.value, 0x0102030405060708)

    def test_little_endian(self):
        packet = Int64Packet.deserialize(b'\x01\x02\x03\x04\x05\x06\x07\x08',
                                         endian=Endian.LITTLE_ENDIAN)
        self.assertEqual(packet.value, 0x0807060504030201)

    def test_varlength(self):
        packet = VarlengthPacket.deserialize(b"\x02\xde\xad")
        self.assertEqual(packet.length, 0x02)
        self.assertEqual(packet.value, b'\xde\xad')

        packet = VarlengthPacket.deserialize(b"\x04\xde\xad\xbe\xef")
        self.assertEqual(packet.length, 0x04)
        self.assertEqual(packet.value, b'\xde\xad\xbe\xef')

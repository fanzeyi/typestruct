# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typestruct import Packet, Endian
from typestruct.types import uint8, uint16, Slice, Varlength


@dataclass
class ICMPPacket(Packet):
    ttype: uint8
    code: uint8
    checksum: uint16
    rest: Slice(4)


packet = ICMPPacket(1, 2, 3, b"abcd")
binary = packet.serialize()
print(binary)  # => b'\x01\x02\x03\x00abcd'

recovered = ICMPPacket.deserialize(binary)
print(recovered)  # => ICMPPacket(ttype=1, code=2, checksum=3, rest=b'abcd')

print(packet.serialize(endian=Endian.BIG_ENDIAN))  # => b'\x01\x02\x00\x03abcd'


@dataclass
class TLV(Packet):
    tag: uint8
    length: uint8
    value: Varlength(lambda s: s.length)


tlv = TLV(tag=1, length=5, value=b"abcde")
binary = tlv.serialize()
print(binary)  # => b'\x01\x05abcde'

recovered = TLV.deserialize(binary)
print(recovered)  # => TLV(tag=1, length=5, value=b'abcde')

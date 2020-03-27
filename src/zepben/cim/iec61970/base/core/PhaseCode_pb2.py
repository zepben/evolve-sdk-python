"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/cim/iec61970/base/core/PhaseCode.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/cim/iec61970/base/core/PhaseCode.proto',
  package='zepben.cim.iec61970.base.core',
  syntax='proto3',
  serialized_options=_b('\n*com.zepben.protobuf.cim.iec61970.base.coreP\001'),
  serialized_pb=_b('\n-zepben/cim/iec61970/base/core/PhaseCode.proto\x12\x1dzepben.cim.iec61970.base.core*\xaf\x01\n\tPhaseCode\x12\x08\n\x04NONE\x10\x00\x12\x05\n\x01\x41\x10\x01\x12\x05\n\x01\x42\x10\x02\x12\x05\n\x01\x43\x10\x03\x12\x05\n\x01N\x10\x04\x12\x06\n\x02\x41\x42\x10\x05\x12\x06\n\x02\x41\x43\x10\x06\x12\x06\n\x02\x41N\x10\x07\x12\x06\n\x02\x42\x43\x10\x08\x12\x06\n\x02\x42N\x10\t\x12\x06\n\x02\x43N\x10\n\x12\x07\n\x03\x41\x42\x43\x10\x0b\x12\x07\n\x03\x41\x42N\x10\x0c\x12\x07\n\x03\x41\x43N\x10\r\x12\x07\n\x03\x42\x43N\x10\x0e\x12\x08\n\x04\x41\x42\x43N\x10\x0f\x12\x05\n\x01X\x10\x10\x12\x06\n\x02XN\x10\x11\x12\x06\n\x02XY\x10\x12\x12\x07\n\x03XYN\x10\x13\x42.\n*com.zepben.protobuf.cim.iec61970.base.coreP\x01\x62\x06proto3')
)

_PHASECODE = _descriptor.EnumDescriptor(
  name='PhaseCode',
  full_name='zepben.cim.iec61970.base.core.PhaseCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='A', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='B', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='C', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='N', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AB', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AC', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AN', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BC', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BN', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CN', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABC', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABN', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACN', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BCN', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABCN', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='X', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='XN', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='XY', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='XYN', index=19, number=19,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=81,
  serialized_end=256,
)
_sym_db.RegisterEnumDescriptor(_PHASECODE)

PhaseCode = enum_type_wrapper.EnumTypeWrapper(_PHASECODE)
NONE = 0
A = 1
B = 2
C = 3
N = 4
AB = 5
AC = 6
AN = 7
BC = 8
BN = 9
CN = 10
ABC = 11
ABN = 12
ACN = 13
BCN = 14
ABCN = 15
X = 16
XN = 17
XY = 18
XYN = 19


DESCRIPTOR.enum_types_by_name['PhaseCode'] = _PHASECODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
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
# source: zepben/cim/iec61970/base/diagramlayout/DiagramObjectStyle.proto

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
  name='zepben/cim/iec61970/base/diagramlayout/DiagramObjectStyle.proto',
  package='zepben.cim.iec61970.base.diagramlayout',
  syntax='proto3',
  serialized_options=_b('\n3com.zepben.protobuf.cim.iec61970.base.diagramlayoutP\001'),
  serialized_pb=_b('\n?zepben/cim/iec61970/base/diagramlayout/DiagramObjectStyle.proto\x12&zepben.cim.iec61970.base.diagramlayout*\xc0\x04\n\x12\x44iagramObjectStyle\x12\x08\n\x04NONE\x10\x00\x12\x14\n\x10\x44IST_TRANSFORMER\x10\x01\x12\x13\n\x0fISO_TRANSFORMER\x10\x02\x12\x18\n\x14REVERSIBLE_REGULATOR\x10\x03\x12\x1c\n\x18NON_REVERSIBLE_REGULATOR\x10\x04\x12\x14\n\x10ZONE_TRANSFORMER\x10\x05\x12\r\n\tFEEDER_CB\x10\x06\x12\x06\n\x02\x43\x42\x10\x07\x12\x0c\n\x08JUNCTION\x10\x08\x12\x10\n\x0c\x44ISCONNECTOR\x10\t\x12\x08\n\x04\x46USE\x10\n\x12\x0c\n\x08RECLOSER\x10\x0b\x12\x13\n\x0f\x46\x41ULT_INDICATOR\x10\x0c\x12\n\n\x06JUMPER\x10\r\x12\x11\n\rENERGY_SOURCE\x10\x0e\x12\x15\n\x11SHUNT_COMPENSATOR\x10\x0f\x12\x0f\n\x0bUSAGE_POINT\x10\x10\x12\x15\n\x11\x43ONDUCTOR_UNKNOWN\x10\x11\x12\x10\n\x0c\x43ONDUCTOR_LV\x10\x12\x12\x12\n\x0e\x43ONDUCTOR_6600\x10\x13\x12\x13\n\x0f\x43ONDUCTOR_11000\x10\x14\x12\x13\n\x0f\x43ONDUCTOR_12700\x10\x15\x12\x13\n\x0f\x43ONDUCTOR_22000\x10\x16\x12\x13\n\x0f\x43ONDUCTOR_33000\x10\x17\x12\x13\n\x0f\x43ONDUCTOR_66000\x10\x18\x12\x14\n\x10\x43ONDUCTOR_132000\x10\x19\x12\x14\n\x10\x43ONDUCTOR_220000\x10\x1a\x12\x14\n\x10\x43ONDUCTOR_275000\x10\x1b\x12\x14\n\x10\x43ONDUCTOR_500000\x10\x1c\x42\x37\n3com.zepben.protobuf.cim.iec61970.base.diagramlayoutP\x01\x62\x06proto3')
)

_DIAGRAMOBJECTSTYLE = _descriptor.EnumDescriptor(
  name='DiagramObjectStyle',
  full_name='zepben.cim.iec61970.base.diagramlayout.DiagramObjectStyle',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DIST_TRANSFORMER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ISO_TRANSFORMER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REVERSIBLE_REGULATOR', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NON_REVERSIBLE_REGULATOR', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ZONE_TRANSFORMER', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEEDER_CB', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CB', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUNCTION', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISCONNECTOR', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FUSE', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECLOSER', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAULT_INDICATOR', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUMPER', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENERGY_SOURCE', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHUNT_COMPENSATOR', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USAGE_POINT', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_UNKNOWN', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_LV', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_6600', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_11000', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_12700', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_22000', index=22, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_33000', index=23, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_66000', index=24, number=24,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_132000', index=25, number=25,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_220000', index=26, number=26,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_275000', index=27, number=27,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONDUCTOR_500000', index=28, number=28,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=108,
  serialized_end=684,
)
_sym_db.RegisterEnumDescriptor(_DIAGRAMOBJECTSTYLE)

DiagramObjectStyle = enum_type_wrapper.EnumTypeWrapper(_DIAGRAMOBJECTSTYLE)
NONE = 0
DIST_TRANSFORMER = 1
ISO_TRANSFORMER = 2
REVERSIBLE_REGULATOR = 3
NON_REVERSIBLE_REGULATOR = 4
ZONE_TRANSFORMER = 5
FEEDER_CB = 6
CB = 7
JUNCTION = 8
DISCONNECTOR = 9
FUSE = 10
RECLOSER = 11
FAULT_INDICATOR = 12
JUMPER = 13
ENERGY_SOURCE = 14
SHUNT_COMPENSATOR = 15
USAGE_POINT = 16
CONDUCTOR_UNKNOWN = 17
CONDUCTOR_LV = 18
CONDUCTOR_6600 = 19
CONDUCTOR_11000 = 20
CONDUCTOR_12700 = 21
CONDUCTOR_22000 = 22
CONDUCTOR_33000 = 23
CONDUCTOR_66000 = 24
CONDUCTOR_132000 = 25
CONDUCTOR_220000 = 26
CONDUCTOR_275000 = 27
CONDUCTOR_500000 = 28


DESCRIPTOR.enum_types_by_name['DiagramObjectStyle'] = _DIAGRAMOBJECTSTYLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

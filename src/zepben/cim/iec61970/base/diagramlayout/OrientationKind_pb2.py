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
# source: zepben/cim/iec61970/base/diagramlayout/OrientationKind.proto

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
  name='zepben/cim/iec61970/base/diagramlayout/OrientationKind.proto',
  package='zepben.cim.iec61970.base.diagramlayout',
  syntax='proto3',
  serialized_options=_b('\n3com.zepben.protobuf.cim.iec61970.base.diagramlayoutP\001'),
  serialized_pb=_b('\n<zepben/cim/iec61970/base/diagramlayout/OrientationKind.proto\x12&zepben.cim.iec61970.base.diagramlayout*-\n\x0fOrientationKind\x12\x0c\n\x08POSITIVE\x10\x00\x12\x0c\n\x08NEGATIVE\x10\x01\x42\x37\n3com.zepben.protobuf.cim.iec61970.base.diagramlayoutP\x01\x62\x06proto3')
)

_ORIENTATIONKIND = _descriptor.EnumDescriptor(
  name='OrientationKind',
  full_name='zepben.cim.iec61970.base.diagramlayout.OrientationKind',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='POSITIVE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEGATIVE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=104,
  serialized_end=149,
)
_sym_db.RegisterEnumDescriptor(_ORIENTATIONKIND)

OrientationKind = enum_type_wrapper.EnumTypeWrapper(_ORIENTATIONKIND)
POSITIVE = 0
NEGATIVE = 1


DESCRIPTOR.enum_types_by_name['OrientationKind'] = _ORIENTATIONKIND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
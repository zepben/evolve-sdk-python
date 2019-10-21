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
# source: zepben/cim/iec61968/common/Organisation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.cim.iec61970.base.diagramlayout import DiagramObject_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/cim/iec61968/common/Organisation.proto',
  package='zepben.cim.iec61968.common',
  syntax='proto3',
  serialized_options=_b('\n\'com.zepben.protobuf.cim.iec61968.commonP\001'),
  serialized_pb=_b('\n-zepben/cim/iec61968/common/Organisation.proto\x12\x1azepben.cim.iec61968.common\x1a:zepben/cim/iec61970/base/diagramlayout/DiagramObject.proto\"y\n\x0cOrganisation\x12\x0c\n\x04mRID\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12M\n\x0e\x64iagramObjects\x18\x10 \x03(\x0b\x32\x35.zepben.cim.iec61970.base.diagramlayout.DiagramObjectB+\n\'com.zepben.protobuf.cim.iec61968.commonP\x01\x62\x06proto3')
  ,
  dependencies=[zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2.DESCRIPTOR,])




_ORGANISATION = _descriptor.Descriptor(
  name='Organisation',
  full_name='zepben.cim.iec61968.common.Organisation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mRID', full_name='zepben.cim.iec61968.common.Organisation.mRID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='zepben.cim.iec61968.common.Organisation.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='diagramObjects', full_name='zepben.cim.iec61968.common.Organisation.diagramObjects', index=2,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=137,
  serialized_end=258,
)

_ORGANISATION.fields_by_name['diagramObjects'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2._DIAGRAMOBJECT
DESCRIPTOR.message_types_by_name['Organisation'] = _ORGANISATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Organisation = _reflection.GeneratedProtocolMessageType('Organisation', (_message.Message,), {
  'DESCRIPTOR' : _ORGANISATION,
  '__module__' : 'zepben.cim.iec61968.common.Organisation_pb2'
  # @@protoc_insertion_point(class_scope:zepben.cim.iec61968.common.Organisation)
  })
_sym_db.RegisterMessage(Organisation)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

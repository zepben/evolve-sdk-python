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
# source: zepben/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto

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
  name='zepben/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto',
  package='zepben.cim.iec61970.base.wires',
  syntax='proto3',
  serialized_options=_b('\n+com.zepben.protobuf.cim.iec61970.base.wiresP\001'),
  serialized_pb=_b('\n?zepben/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto\x12\x1ezepben.cim.iec61970.base.wires\x1a:zepben/cim/iec61970/base/diagramlayout/DiagramObject.proto\"\xd0\x01\n\x1aPerLengthSequenceImpedance\x12\x0c\n\x04mRID\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\t\n\x01r\x18\x03 \x01(\x01\x12\t\n\x01x\x18\x04 \x01(\x01\x12\n\n\x02r0\x18\x05 \x01(\x01\x12\n\n\x02x0\x18\x06 \x01(\x01\x12\x0b\n\x03\x62\x63h\x18\x07 \x01(\x01\x12\x0c\n\x04\x62\x30\x63h\x18\x08 \x01(\x01\x12M\n\x0e\x64iagramObjects\x18\x10 \x03(\x0b\x32\x35.zepben.cim.iec61970.base.diagramlayout.DiagramObjectB/\n+com.zepben.protobuf.cim.iec61970.base.wiresP\x01\x62\x06proto3')
  ,
  dependencies=[zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2.DESCRIPTOR,])




_PERLENGTHSEQUENCEIMPEDANCE = _descriptor.Descriptor(
  name='PerLengthSequenceImpedance',
  full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mRID', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.mRID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='r', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.r', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.x', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='r0', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.r0', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x0', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.x0', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bch', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.bch', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='b0ch', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.b0ch', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='diagramObjects', full_name='zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance.diagramObjects', index=8,
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
  serialized_start=160,
  serialized_end=368,
)

_PERLENGTHSEQUENCEIMPEDANCE.fields_by_name['diagramObjects'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2._DIAGRAMOBJECT
DESCRIPTOR.message_types_by_name['PerLengthSequenceImpedance'] = _PERLENGTHSEQUENCEIMPEDANCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PerLengthSequenceImpedance = _reflection.GeneratedProtocolMessageType('PerLengthSequenceImpedance', (_message.Message,), {
  'DESCRIPTOR' : _PERLENGTHSEQUENCEIMPEDANCE,
  '__module__' : 'zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2'
  # @@protoc_insertion_point(class_scope:zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance)
  })
_sym_db.RegisterMessage(PerLengthSequenceImpedance)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

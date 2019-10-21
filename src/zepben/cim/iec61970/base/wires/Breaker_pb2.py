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
# source: zepben/cim/iec61970/base/wires/Breaker.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.cim.iec61968.common import Location_pb2 as zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2
from zepben.cim.iec61970.base.core import Terminal_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2
from zepben.cim.iec61970.base.diagramlayout import DiagramObject_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2
from zepben.cim.iec61970.base.meas import Control_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2
from zepben.cim.iec61970.base.meas import Measurement_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/cim/iec61970/base/wires/Breaker.proto',
  package='zepben.cim.iec61970.base.wires',
  syntax='proto3',
  serialized_options=_b('\n+com.zepben.protobuf.cim.iec61970.base.wiresP\001'),
  serialized_pb=_b('\n,zepben/cim/iec61970/base/wires/Breaker.proto\x12\x1ezepben.cim.iec61970.base.wires\x1a)zepben/cim/iec61968/common/Location.proto\x1a,zepben/cim/iec61970/base/core/Terminal.proto\x1a:zepben/cim/iec61970/base/diagramlayout/DiagramObject.proto\x1a+zepben/cim/iec61970/base/meas/Control.proto\x1a/zepben/cim/iec61970/base/meas/Measurement.proto\"\xe2\x03\n\x07\x42reaker\x12\x0c\n\x04mRID\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tinService\x18\x03 \x01(\x08\x12\x19\n\x11normallyInService\x18\x04 \x01(\x08\x12\x17\n\x0f\x62\x61seVoltageMRID\x18\x05 \x01(\t\x12:\n\tterminals\x18\x06 \x03(\x0b\x32\'.zepben.cim.iec61970.base.core.Terminal\x12\x12\n\nnormalOpen\x18\x07 \x03(\x08\x12\x0c\n\x04open\x18\x08 \x03(\x08\x12M\n\x0e\x64iagramObjects\x18\x10 \x03(\x0b\x32\x35.zepben.cim.iec61970.base.diagramlayout.DiagramObject\x12\x15\n\rassetInfoMRID\x18\x11 \x01(\t\x12\x36\n\x08location\x18\x12 \x01(\x0b\x32$.zepben.cim.iec61968.common.Location\x12\x37\n\x07\x63ontrol\x18\x13 \x01(\x0b\x32&.zepben.cim.iec61970.base.meas.Control\x12?\n\x0bmeasurement\x18\x14 \x01(\x0b\x32*.zepben.cim.iec61970.base.meas.MeasurementB/\n+com.zepben.protobuf.cim.iec61970.base.wiresP\x01\x62\x06proto3')
  ,
  dependencies=[zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2.DESCRIPTOR,])




_BREAKER = _descriptor.Descriptor(
  name='Breaker',
  full_name='zepben.cim.iec61970.base.wires.Breaker',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mRID', full_name='zepben.cim.iec61970.base.wires.Breaker.mRID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='zepben.cim.iec61970.base.wires.Breaker.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inService', full_name='zepben.cim.iec61970.base.wires.Breaker.inService', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='normallyInService', full_name='zepben.cim.iec61970.base.wires.Breaker.normallyInService', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='baseVoltageMRID', full_name='zepben.cim.iec61970.base.wires.Breaker.baseVoltageMRID', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='terminals', full_name='zepben.cim.iec61970.base.wires.Breaker.terminals', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='normalOpen', full_name='zepben.cim.iec61970.base.wires.Breaker.normalOpen', index=6,
      number=7, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='open', full_name='zepben.cim.iec61970.base.wires.Breaker.open', index=7,
      number=8, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='diagramObjects', full_name='zepben.cim.iec61970.base.wires.Breaker.diagramObjects', index=8,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='assetInfoMRID', full_name='zepben.cim.iec61970.base.wires.Breaker.assetInfoMRID', index=9,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location', full_name='zepben.cim.iec61970.base.wires.Breaker.location', index=10,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control', full_name='zepben.cim.iec61970.base.wires.Breaker.control', index=11,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='measurement', full_name='zepben.cim.iec61970.base.wires.Breaker.measurement', index=12,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=324,
  serialized_end=806,
)

_BREAKER.fields_by_name['terminals'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2._TERMINAL
_BREAKER.fields_by_name['diagramObjects'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2._DIAGRAMOBJECT
_BREAKER.fields_by_name['location'].message_type = zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2._LOCATION
_BREAKER.fields_by_name['control'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2._CONTROL
_BREAKER.fields_by_name['measurement'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2._MEASUREMENT
DESCRIPTOR.message_types_by_name['Breaker'] = _BREAKER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Breaker = _reflection.GeneratedProtocolMessageType('Breaker', (_message.Message,), {
  'DESCRIPTOR' : _BREAKER,
  '__module__' : 'zepben.cim.iec61970.base.wires.Breaker_pb2'
  # @@protoc_insertion_point(class_scope:zepben.cim.iec61970.base.wires.Breaker)
  })
_sym_db.RegisterMessage(Breaker)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

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
# source: zepben/cim/iec61970/base/core/Feeder.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.cim.iec61968.common import Location_pb2 as zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2
from zepben.cim.iec61970.base.diagramlayout import DiagramObject_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2
from zepben.cim.iec61970.base.meas import Control_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2
from zepben.cim.iec61970.base.meas import Measurement_pb2 as zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/cim/iec61970/base/core/Feeder.proto',
  package='zepben.cim.iec61970.base.core',
  syntax='proto3',
  serialized_options=_b('\n*com.zepben.protobuf.cim.iec61970.base.coreP\001'),
  serialized_pb=_b('\n*zepben/cim/iec61970/base/core/Feeder.proto\x12\x1dzepben.cim.iec61970.base.core\x1a)zepben/cim/iec61968/common/Location.proto\x1a:zepben/cim/iec61970/base/diagramlayout/DiagramObject.proto\x1a+zepben/cim/iec61970/base/meas/Control.proto\x1a/zepben/cim/iec61970/base/meas/Measurement.proto\"\xbb\x03\n\x06\x46\x65\x65\x64\x65r\x12\x0c\n\x04mRID\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0e\x65quipmentMRIDs\x18\x03 \x03(\t\x12\x1e\n\x16normalHeadTerminalMRID\x18\x04 \x01(\t\x12&\n\x1enormalEnergizingSubstationMRID\x18\x05 \x01(\t\x12\x1d\n\x15\x63urrentEquipmentMRIDs\x18\x06 \x03(\t\x12M\n\x0e\x64iagramObjects\x18\x10 \x03(\x0b\x32\x35.zepben.cim.iec61970.base.diagramlayout.DiagramObject\x12\x15\n\rassetInfoMRID\x18\x11 \x01(\t\x12\x36\n\x08location\x18\x12 \x01(\x0b\x32$.zepben.cim.iec61968.common.Location\x12\x37\n\x07\x63ontrol\x18\x13 \x01(\x0b\x32&.zepben.cim.iec61970.base.meas.Control\x12?\n\x0bmeasurement\x18\x14 \x01(\x0b\x32*.zepben.cim.iec61970.base.meas.MeasurementB.\n*com.zepben.protobuf.cim.iec61970.base.coreP\x01\x62\x06proto3')
  ,
  dependencies=[zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2.DESCRIPTOR,zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2.DESCRIPTOR,])




_FEEDER = _descriptor.Descriptor(
  name='Feeder',
  full_name='zepben.cim.iec61970.base.core.Feeder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mRID', full_name='zepben.cim.iec61970.base.core.Feeder.mRID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='zepben.cim.iec61970.base.core.Feeder.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='equipmentMRIDs', full_name='zepben.cim.iec61970.base.core.Feeder.equipmentMRIDs', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='normalHeadTerminalMRID', full_name='zepben.cim.iec61970.base.core.Feeder.normalHeadTerminalMRID', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='normalEnergizingSubstationMRID', full_name='zepben.cim.iec61970.base.core.Feeder.normalEnergizingSubstationMRID', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currentEquipmentMRIDs', full_name='zepben.cim.iec61970.base.core.Feeder.currentEquipmentMRIDs', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='diagramObjects', full_name='zepben.cim.iec61970.base.core.Feeder.diagramObjects', index=6,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='assetInfoMRID', full_name='zepben.cim.iec61970.base.core.Feeder.assetInfoMRID', index=7,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location', full_name='zepben.cim.iec61970.base.core.Feeder.location', index=8,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control', full_name='zepben.cim.iec61970.base.core.Feeder.control', index=9,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='measurement', full_name='zepben.cim.iec61970.base.core.Feeder.measurement', index=10,
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
  serialized_start=275,
  serialized_end=718,
)

_FEEDER.fields_by_name['diagramObjects'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2._DIAGRAMOBJECT
_FEEDER.fields_by_name['location'].message_type = zepben_dot_cim_dot_iec61968_dot_common_dot_Location__pb2._LOCATION
_FEEDER.fields_by_name['control'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Control__pb2._CONTROL
_FEEDER.fields_by_name['measurement'].message_type = zepben_dot_cim_dot_iec61970_dot_base_dot_meas_dot_Measurement__pb2._MEASUREMENT
DESCRIPTOR.message_types_by_name['Feeder'] = _FEEDER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Feeder = _reflection.GeneratedProtocolMessageType('Feeder', (_message.Message,), {
  'DESCRIPTOR' : _FEEDER,
  '__module__' : 'zepben.cim.iec61970.base.core.Feeder_pb2'
  # @@protoc_insertion_point(class_scope:zepben.cim.iec61970.base.core.Feeder)
  })
_sym_db.RegisterMessage(Feeder)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

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
# source: zepben/cim/iec61968/customers/CustomerKind.proto

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
  name='zepben/cim/iec61968/customers/CustomerKind.proto',
  package='zepben.cim.iec61968.customers',
  syntax='proto3',
  serialized_options=_b('\n*com.zepben.protobuf.cim.iec61968.customersP\001'),
  serialized_pb=_b('\n0zepben/cim/iec61968/customers/CustomerKind.proto\x12\x1dzepben.cim.iec61968.customers*\xdf\x02\n\x0c\x43ustomerKind\x12\x18\n\x14\x63ommercialIndustrial\x10\x00\x12\x1a\n\x16\x65nergyServiceScheduler\x10\x01\x12\x19\n\x15\x65nergyServiceSupplier\x10\x02\x12\x0e\n\nenterprise\x10\x03\x12\x0f\n\x0binternalUse\x10\x04\x12\t\n\x05other\x10\x05\x12\x0f\n\x0bpumpingLoad\x10\x06\x12\x14\n\x10regionalOperator\x10\x07\x12\x0f\n\x0bresidential\x10\x08\x12\x1c\n\x18residentialAndCommercial\x10\t\x12\x1d\n\x19residentialAndStreetlight\x10\n\x12\x1a\n\x16residentialFarmService\x10\x0b\x12 \n\x1cresidentialStreetlightOthers\x10\x0c\x12\x0e\n\nsubsidiary\x10\r\x12\x0f\n\x0bwindMachine\x10\x0e\x42.\n*com.zepben.protobuf.cim.iec61968.customersP\x01\x62\x06proto3')
)

_CUSTOMERKIND = _descriptor.EnumDescriptor(
  name='CustomerKind',
  full_name='zepben.cim.iec61968.customers.CustomerKind',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='commercialIndustrial', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='energyServiceScheduler', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='energyServiceSupplier', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='enterprise', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='internalUse', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='other', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='pumpingLoad', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='regionalOperator', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='residential', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='residentialAndCommercial', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='residentialAndStreetlight', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='residentialFarmService', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='residentialStreetlightOthers', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='subsidiary', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='windMachine', index=14, number=14,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=84,
  serialized_end=435,
)
_sym_db.RegisterEnumDescriptor(_CUSTOMERKIND)

CustomerKind = enum_type_wrapper.EnumTypeWrapper(_CUSTOMERKIND)
commercialIndustrial = 0
energyServiceScheduler = 1
energyServiceSupplier = 2
enterprise = 3
internalUse = 4
other = 5
pumpingLoad = 6
regionalOperator = 7
residential = 8
residentialAndCommercial = 9
residentialAndStreetlight = 10
residentialFarmService = 11
residentialStreetlightOthers = 12
subsidiary = 13
windMachine = 14


DESCRIPTOR.enum_types_by_name['CustomerKind'] = _CUSTOMERKIND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

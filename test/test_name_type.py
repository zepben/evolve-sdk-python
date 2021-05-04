#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.model.cim.iec61970.base.core import identified_object

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.model.cim.iec61970.base.wires.connectors import Junction

#class test_name_type():
##reason for nested functions in class??

def test_constructor_coverage():
    assert NameType("name", "description").name == "name"
    ##Check NameType definition is correct

def test_name_and_description():
    name_type = NameType("name", "description")
    assert name_type.name == "name"
    assert name_type.description == "description"

    name_type.name = "name"
    name_type.description = "description"

    assert name_type.name == "name"
    assert name_type.description == "description"

def test_gets_adds_names():
    name_type = NameType("type","description")
    id_obj_1 = Junction()
    name1 = name_type.get_or_add_name("name1", id_obj_1)
    assert name1 == name_type.get_or_add_name("name1",id_obj_1)
    #NameError: name 'Name' is not defined
    assert name_type.has_name("name1")



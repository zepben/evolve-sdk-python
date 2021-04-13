#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections.abc import MutableMapping

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

## @property name Name of the name type.
## @property description Description of the name type.

class NameType(name):
    """
    Type of name. Possible values for attribute 'name' are implementation dependent but standard profiles may specify types. An enterprise may have multiple
    IT systems each having its own local name for the same object, e.g. a planning system may have different names from an EMS. An object may also have
    different names within the same IT system, e.g. localName as defined in CIM version 14. The definition from CIM14 is:
    The localName is a human readable name of the object. It is a free text name local to a node in a naming hierarchy similar to a file directory structure.
    A power system related naming hierarchy may be: Substation, VoltageLevel, Equipment etc. Children of the same parent in such a hierarchy have names that
    typically are unique among them.
    """
    def __init__(self):

        self.names_index = {}
        self.names_multi_index = {}
        self.description = ""

    names_index = __names_index
    names_multi_index = __names_multi_index
    names_index_values = __names_index.values()
    names_multi_index_values = sorted({x for value in __names_multi_index.values() for x in value})
    names = list(names_index_values)
    names = names.append(names_multi_index_values)

    ##  The names for this name type.

    def _has_name(self):
        if name in __namesIndex or name in __names_multi_index:
            return True
        else:
            return False

    ## Get all the [Name] instances for the provided [name].
    ## @return A list of [Name]

    def _get_names(name):
        __names_index[name]

    def _get_or_add_name(name):
        if __names_index.has_key() == True:
        existing = __names_index[name]


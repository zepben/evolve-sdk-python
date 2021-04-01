#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

class nameType(IdentifiedObject):
    """
    Type of name. Possible values for attribute 'name' are implementation dependent but standard profiles may specify types. An enterprise may have multiple
    IT systems each having its own local name for the same object, e.g. a planning system may have different names from an EMS. An object may also have
    different names within the same IT system, e.g. localName as defined in CIM version 14. The definition from CIM14 is:
    The localName is a human readable name of the object. It is a free text name local to a node in a naming hierarchy similar to a file directory structure.
    A power system related naming hierarchy may be: Substation, VoltageLevel, Equipment etc. Children of the same parent in such a hierarchy have names that
    typically are unique among them.
    """


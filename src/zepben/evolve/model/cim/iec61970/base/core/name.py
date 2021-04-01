#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclassy import dataclass
if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
    from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType


@dataclass()
class Name():
    """
    The Name class provides the means to define any number of human readable names for an object. A name is **not** to be used for defining inter-object
    relationships. For inter-object relationships instead use the object identification 'mRID'.

    @property name Any free text that name the object.
    @property type [NameType] for the object
    @property identifiedObject [IdentifiedObject] for the object
    """

    name: str

    type: NameType

    identified_object: IdentifiedObject

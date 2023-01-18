#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING, Iterable

from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.util import get_by_mrid, ngen, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.evolve import ProtectionEquipment, RecloseSequence


__all__ = ["ProtectedSwitch"]


class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by ProtectionEquipment.
    """

    breaking_capacity: Optional[int] = None
    """The maximum fault current in amps a breaking device can break safely under prescribed conditions of use."""

    _reclose_sequences: Optional[List[RecloseSequence]] = None
    _operated_by_protection_equipment: Optional[List[ProtectionEquipment]] = None

    def __init__(
        self,
        reclose_sequences: Iterable[RecloseSequence] = None,
        operated_by_protection_equipment: Iterable[ProtectionEquipment] = None,
        **kwargs
    ):
        super(ProtectedSwitch, self).__init__(**kwargs)

        # breaking_capacity is handled via dataclassy.
        if reclose_sequences is not None:
            for reclose_sequence in reclose_sequences:
                self.add_reclose_sequence(reclose_sequence)
        if operated_by_protection_equipment is not None:
            for protection_equipment in operated_by_protection_equipment:
                self.add_operated_by_protection_equipment(protection_equipment)

    @property
    def reclose_sequences(self) -> Generator[RecloseSequence, None, None]:
        """
        Yields all :class:`RecloseSequence`'s attached to this :class:`ProtectedSwitch`.

        :return: A generator that iterates over all RecloseSequences attached to this ProtectedSwitch.
        """
        return ngen(self._reclose_sequences)

    def num_reclose_sequences(self) -> int:
        """
        Get the number of :class:`RecloseSequence`'s attached to this :class:`ProtectedSwitch`.

        :return: The number of RecloseSequences attached to this ProtectedSwitch.
        """
        return nlen(self._reclose_sequences)

    def get_reclose_sequence(self, mrid: str) -> Optional[RecloseSequence]:
        """
        Get a :class:`RecloseSequence` attached to this :class:`ProtectedSwitch` with the specified `mrid`.

        :param mrid: The mRID of the desired RecloseSequence
        :return: The RecloseSequence with the specified mRID if it exists, otherwise None.
        """
        return get_by_mrid(self._reclose_sequences, mrid)

    def add_reclose_sequence(self, reclose_sequence: RecloseSequence) -> ProtectedSwitch:
        """
        Add a :class:`RecloseSequence` to this :class:`ProtectedSwitch`.
        :param reclose_sequence: The RecloseSequence to add to this ProtectedSwitch.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        if self._validate_reference(reclose_sequence, self.get_reclose_sequence, "A RecloseSequence"):
            return self

        self._reclose_sequences = list() if self._reclose_sequences is None else self._reclose_sequences
        self._reclose_sequences.append(reclose_sequence)

        return self

    def remove_reclose_sequence(self, reclose_sequence: Optional[RecloseSequence]) -> ProtectedSwitch:
        """
        Remove a :class:`RecloseSequence` from this :class:`ProtectedSwitch`.
        :param reclose_sequence: The RecloseSequence to remove from this ProtectedSwitch.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        self._reclose_sequences = safe_remove(self._reclose_sequences, reclose_sequence)
        return self

    def clear_reclose_sequences(self) -> ProtectedSwitch:
        """
        Clear all :class:`RecloseSequence`'s from this :class:`ProtectedSwitch`.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        self._reclose_sequences = None
        return self

    @property
    def operated_by_protection_equipment(self) -> Generator[ProtectionEquipment, None, None]:
        """
        Yields all :class:`ProtectionEquipment` operating this :class:`ProtectedSwitch`.

        :return: A generator that iterates over all ProtectionEquipment operating this ProtectedSwitch.
        """
        return ngen(self._operated_by_protection_equipment)

    def num_operated_by_protection_equipment(self) -> int:
        """
        Get the number of :class:`ProtectionEquipment` operating this :class:`ProtectedSwitch`.

        :return: The number of ProtectionEquipment operating this ProtectedSwitch.
        """
        return nlen(self._operated_by_protection_equipment)

    def get_operated_by_protection_equipment(self, mrid: str) -> Optional[ProtectionEquipment]:
        """
        Get a :class:`ProtectionEquipment` operating this :class:`ProtectedSwitch` with the specified `mrid`.

        :param mrid: The mRID of the desired ProtectionEquipment
        :return: The ProtectionEquipment with the specified mRID if it exists, otherwise None.
        """
        return get_by_mrid(self._operated_by_protection_equipment, mrid)

    def add_operated_by_protection_equipment(self, operated_by_protection_equipment: ProtectionEquipment) -> ProtectedSwitch:
        """
        Associate this :class:`ProtectedSwitch` with a :class:`ProtectionEquipment` operating it.
        :param operated_by_protection_equipment: The ProtectionEquipment to associate with this ProtectedSwitch.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        if self._validate_reference(operated_by_protection_equipment, self.get_operated_by_protection_equipment, "A ProtectionEquipment"):
            return self

        self._operated_by_protection_equipment = list() if self._operated_by_protection_equipment is None else self._operated_by_protection_equipment
        self._operated_by_protection_equipment.append(operated_by_protection_equipment)

        return self

    def remove_operated_by_protection_equipment(self, operated_by_protection_equipment: Optional[ProtectionEquipment]) -> ProtectedSwitch:
        """
        Disassociate this :class:`ProtectedSwitch` from a :class:`ProtectionEquipment`.
        :param operated_by_protection_equipment: The ProtectionEquipment to disassociate from this ProtectedSwitch.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        self._operated_by_protection_equipment = safe_remove(self._operated_by_protection_equipment, operated_by_protection_equipment)
        return self

    def clear_operated_by_protection_equipment(self) -> ProtectedSwitch:
        """
        Disassociate all :class:`ProtectionEquipment` from this :class:`ProtectedSwitch`.
        :return: A reference to this ProtectedSwitch for fluent use.
        """
        self._operated_by_protection_equipment = None
        return self

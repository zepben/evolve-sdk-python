#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import List, Optional, Generator

from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.util import nlen, ngen, get_by_mrid, safe_remove

__all__ = ["PowerTransformerInfo"]


class PowerTransformerInfo(AssetInfo):
    """Set of power transformer data, from an equipment library."""

    _transformer_tank_infos: Optional[List[TransformerTankInfo]] = None
    """Data for all the tanks described by this power transformer data."""

    def __init__(self, transformer_tank_infos: List[TransformerTankInfo] = None):
        if transformer_tank_infos:
            for ti in transformer_tank_infos:
                self.add_transformer_tank_info(ti)

    def num_transformer_tank_infos(self):
        """
        Get the number of `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo`s associated with this `PowerTransformerInfo`.
        """
        return nlen(self._transformer_tank_infos)

    @property
    def transformer_tank_infos(self) -> Generator[TransformerTankInfo, None, None]:
        """
        The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo`s of this `PowerTransformerInfo`.
        """
        return ngen(self._transformer_tank_infos)

    def get_transformer_tank_info(self, mrid: str) -> TransformerTankInfo:
        """
        Get the `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` for this `PowerTransformerInfo` identified by `mrid`.

        `mrid` the mRID of the required `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo`
        Returns The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._transformer_tank_infos, mrid)

    def add_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        """
        `tti` The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` to
        associate with this `PowerTransformerInfo`.
        Returns A reference to this `PowerTransformerInfo` to allow fluent use.
        Raises `ValueError` if another `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` with the same `mrid` already exists in this `PowerTransformerInfo`
        """
        if self._validate_reference(tti, self.get_transformer_tank_info, "A TransformerTankInfo"):
            return self

        self._transformer_tank_infos = list() if self._transformer_tank_infos is None else self._transformer_tank_infos
        self._transformer_tank_infos.append(tti)
        return self

    def remove_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        """
        Disassociate an `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` from this `PowerTransformerInfo`.

        `tti` the `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo` to
        disassociate with this `PowerTransformerInfo`.
        Raises `ValueError` if `tti` was not associated with this `PowerTransformerInfo`.
        Returns A reference to this `Asset` to allow fluent use.
        """
        self._transformer_tank_infos = safe_remove(self._transformer_tank_infos, tti)
        return self

    def clear_transformer_tank_infos(self) -> PowerTransformerInfo:
        """
        Clears all `zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info.TransformerTankInfo`.
        Returns self
        """
        self._transformer_tank_infos = None
        return self

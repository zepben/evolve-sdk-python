#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableEnergySourcePhases"]


class TableEnergySourcePhases(TablePowerSystemResources):

    def __init__(self):
        super(TableEnergySourcePhases, self).__init__()
        self.energy_source_mrid: Column = self._create_column("energy_source_mrid", "TEXT", Nullable.NOT_NULL)
        self.phase: Column = self._create_column("phase", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "energy_source_phases"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergySourcePhases, self).unique_index_columns
        cols.append([self.energy_source_mrid, self.phase])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergySourcePhases, self).non_unique_index_columns
        cols.append([self.energy_source_mrid])
        return cols

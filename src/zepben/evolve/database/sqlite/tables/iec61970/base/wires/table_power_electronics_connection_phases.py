#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TablePowerElectronicsConnectionsPhases"]


class TablePowerElectronicsConnectionsPhases(TablePowerSystemResources):

    def __init__(self):
        super(TablePowerElectronicsConnectionsPhases, self).__init__()
        self.power_electronics_connection_mrid: Column = self._create_column("power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        self.phase: Column = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "power_electronics_connection_phases"

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerElectronicsConnectionsPhases, self).non_unique_index_columns
        cols.append([self.power_electronics_connection_mrid])
        return cols

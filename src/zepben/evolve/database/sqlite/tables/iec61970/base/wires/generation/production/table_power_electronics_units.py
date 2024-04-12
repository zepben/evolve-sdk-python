#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import List

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment import TableEquipment

__all__ = ["TablePowerElectronicsUnits"]


class TablePowerElectronicsUnits(TableEquipment, ABC):

    def __init__(self):
        super(TablePowerElectronicsUnits, self).__init__()
        self.power_electronics_connection_mrid: Column = self._create_column("power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.max_p: Column = self._create_column("max_p", "INTEGER", Nullable.NULL)
        self.min_p: Column = self._create_column("min_p", "INTEGER", Nullable.NULL)

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerElectronicsUnits, self).non_unique_index_columns
        cols.append([self.power_electronics_connection_mrid])
        return cols

#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_ac_dc_terminals import TableAcDcTerminals

__all__ = ["TableTerminals"]


class TableTerminals(TableAcDcTerminals):

    def __init__(self):
        super(TableTerminals, self).__init__()
        self.conducting_equipment_mrid: Column = self._create_column("conducting_equipment_mrid", "TEXT", Nullable.NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.connectivity_node_mrid: Column = self._create_column("connectivity_node_mrid", "TEXT", Nullable.NULL)
        self.phases: Column = self._create_column("phases", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "terminals"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTerminals, self).unique_index_columns
        cols.append([self.conducting_equipment_mrid, self.sequence_number])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTerminals, self).non_unique_index_columns
        cols.append([self.connectivity_node_mrid])
        return cols

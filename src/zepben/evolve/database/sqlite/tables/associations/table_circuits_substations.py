#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TableCircuitsSubstations"]


class TableCircuitsSubstations(SqliteTable):

    def __init__(self):
        super(TableCircuitsSubstations, self).__init__()
        self.circuit_mrid: Column = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        self.substation_mrid: Column = self._create_column("substation_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "circuits_substations"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsSubstations, self).unique_index_columns
        cols.append([self.circuit_mrid, self.substation_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsSubstations, self).non_unique_index_columns
        cols.append([self.circuit_mrid])
        cols.append([self.substation_mrid])
        return cols

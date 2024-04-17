#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableLoopsSubstations"]


class TableLoopsSubstations(SqliteTable):

    def __init__(self):
        super(TableLoopsSubstations, self).__init__()
        self.loop_mrid: Column = self._create_column("loop_mrid", "TEXT", Nullable.NOT_NULL)
        self.substation_mrid: Column = self._create_column("substation_mrid", "TEXT", Nullable.NOT_NULL)
        self.relationship: Column = self._create_column("relationship", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "loops_substations"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableLoopsSubstations, self).unique_index_columns
        cols.append([self.loop_mrid, self.substation_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableLoopsSubstations, self).non_unique_index_columns
        cols.append([self.loop_mrid])
        cols.append([self.substation_mrid])
        return cols

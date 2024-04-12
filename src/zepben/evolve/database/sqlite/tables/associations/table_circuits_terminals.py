#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TableCircuitsTerminals"]


class TableCircuitsTerminals(SqliteTable):

    def __init__(self):
        super(TableCircuitsTerminals, self).__init__()
        self.circuit_mrid: Column = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        self.terminal_mrid: Column = self._create_column("terminal_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "circuits_terminals"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsTerminals, self).unique_index_columns
        cols.append([self.circuit_mrid, self.terminal_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsTerminals, self).non_unique_index_columns
        cols.append([self.circuit_mrid])
        cols.append([self.terminal_mrid])
        return cols

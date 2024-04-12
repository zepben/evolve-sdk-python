#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_lines import TableLines

__all__ = ["TableCircuits"]


class TableCircuits(TableLines):

    def __init__(self):
        super(TableCircuits, self).__init__()
        self.loop_mrid: Column = self._create_column("loop_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "circuits"

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuits, self).non_unique_index_columns
        cols.append([self.loop_mrid])
        return cols

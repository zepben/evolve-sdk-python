#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableDiagramObjectPoints"]


class TableDiagramObjectPoints(SqliteTable):

    def __init__(self):
        super(TableDiagramObjectPoints, self).__init__()
        self.diagram_object_mrid: Column = self._create_column("diagram_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.x_position: Column = self._create_column("x_position", "NUMBER", Nullable.NULL)
        self.y_position: Column = self._create_column("y_position", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "diagram_object_points"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableDiagramObjectPoints, self).unique_index_columns
        cols.append([self.diagram_object_mrid, self.sequence_number])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableDiagramObjectPoints, self).non_unique_index_columns
        cols.append([self.diagram_object_mrid])
        return cols

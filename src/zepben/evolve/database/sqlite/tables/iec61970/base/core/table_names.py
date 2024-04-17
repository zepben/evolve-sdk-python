#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableNames"]


class TableNames(SqliteTable):

    def __init__(self):
        super(TableNames, self).__init__()
        self.name_: Column = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.identified_object_mrid: Column = self._create_column("identified_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.name_type_name: Column = self._create_column("name_type_name", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "names"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNames, self).unique_index_columns
        cols.append([self.identified_object_mrid, self.name_type_name, self.name_])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNames, self).non_unique_index_columns
        cols.append([self.identified_object_mrid])
        cols.append([self.name_])
        cols.append([self.name_type_name])
        return cols

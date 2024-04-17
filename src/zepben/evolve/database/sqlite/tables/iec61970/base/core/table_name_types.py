#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

__all__ = ["TableNameTypes"]

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


class TableNameTypes(SqliteTable):

    def __init__(self):
        super(TableNameTypes, self).__init__()
        self.name_: Column = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.description: Column = self._create_column("description", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "name_types"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNameTypes, self).unique_index_columns
        cols.append([self.name_])
        return cols

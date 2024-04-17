#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableRecloseDelays"]


class TableRecloseDelays(SqliteTable):

    def __init__(self):
        super(TableRecloseDelays, self).__init__()
        self.relay_info_mrid: Column = self._create_column("relay_info_mrid", "TEXT", Nullable.NOT_NULL)
        self.reclose_delay: Column = self._create_column("reclose_delay", "NUMBER", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "reclose_delays"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableRecloseDelays, self).unique_index_columns
        cols.append([self.relay_info_mrid, self.sequence_number])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableRecloseDelays, self).non_unique_index_columns
        cols.append([self.relay_info_mrid])
        return cols

    @property
    def select_sql(self):
        return f"{super(TableRecloseDelays, self).select_sql} ORDER BY relay_info_mrid, sequence_number ASC;"
